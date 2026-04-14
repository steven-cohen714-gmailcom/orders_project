# backend/endpoints/evolution_export.py
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os, csv, hashlib

from backend.database import get_db_connection

router = APIRouter(prefix="/evo", tags=["evolution-export"])

# ---------- Models ----------
class StagingRow(BaseModel):
    order_item_id: int
    item_code: str
    supplier_name: Optional[str] = ""
    project: Optional[str] = ""
    order_number: str

    # Editable fields
    date: str                   # 'YYYY/MM/DD'
    reference: str
    description: str
    warehouse_code: str
    transaction_code: str
    gl_contra_account: str
    qty_in: float
    qty_out: Optional[float] = 0.0
    new_cost: Optional[float] = None
    project_code: Optional[str] = None
    job_code: Optional[str] = None
    lot_number: Optional[str] = None

class ExportPayload(BaseModel):
    rows: List[StagingRow]
    notes: Optional[str] = ""

class UnflagPayload(BaseModel):
    order_item_ids: List[int]

# ---------- Helpers ----------
CSV_DIR = "data/exports"
os.makedirs(CSV_DIR, exist_ok=True)

CSV_HEADERS = [
    "Item Code","Warehouse Code","Date","Reference","Description",
    "Quantity In","Quantity Out","New Cost","Transaction Code",
    "Project Code","Job Code","GL Contra Account","Lot Number"
]

def ymd_to_export(date_iso: str, fmt: str) -> str:
    # fmt currently 'YYYY/MM/DD' only, but keep it pluggable
    dt = datetime.fromisoformat(date_iso.replace("Z","").replace(" ", "T")) if "T" in date_iso else datetime.fromisoformat(date_iso)
    return dt.strftime("%Y/%m/%d")

def sha1_row(values: List[Any]) -> str:
    b = "|".join("" if v is None else str(v) for v in values).encode("utf-8")
    return hashlib.sha1(b).hexdigest()

def get_settings(conn):
    c = conn.cursor()
    row = c.execute("SELECT * FROM evo_export_settings WHERE id=1").fetchone()
    if not row:
        # Fallback defaults if seeding somehow failed
        return {
            "default_transaction_code": "JNL",
            "default_gl_contra_account": "9999-000",
            "default_warehouse_code": "MAIN",
            "date_format": "YYYY/MM/DD",
            "description_template": "PO {order_number} – {supplier_name}",
            "encoding": "utf-8",
        }
    return dict(row)

def apply_template(template: str, ctx: Dict[str, Any]) -> str:
    out = template
    for k, v in ctx.items():
        out = out.replace("{"+k+"}", "" if v is None else str(v))
    return out

# ---------- Endpoints ----------

@router.get("/staging")
def get_staging(
    from_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    to_date: Optional[str]   = Query(None, description="YYYY-MM-DD"),
    supplier: Optional[str]  = Query(None),
    project: Optional[str]   = Query(None),
    q: Optional[str]         = Query(None),
    limit: int               = Query(500, ge=1, le=5000),
):
    """
    Returns unexported order items with prefilled defaults for Evolution CSV.
    Includes deleted/any-status orders. 80/20: orders.created_date window.
    """
    with get_db_connection() as conn:
        settings = get_settings(conn)
        c = conn.cursor()

        # Date filters (default last 7 days)
        if not from_date or not to_date:
            to_dt = datetime.utcnow()
            from_dt = to_dt - timedelta(days=7)
            from_date = from_dt.strftime("%Y-%m-%d")
            to_date   = to_dt.strftime("%Y-%m-%d")

        sql = """
        SELECT
            oi.id AS order_item_id,
            oi.item_code, oi.project,
            COALESCE(oi.qty_ordered, 0) AS qty_ordered,
            o.order_number, o.created_date, o.status,
            s.name AS supplier_name,
            p.project_code AS project_code
        FROM order_items oi
        JOIN orders o ON o.id = oi.order_id
        LEFT JOIN suppliers s ON s.id = o.supplier_id
        LEFT JOIN projects p ON p.project_code = oi.project
        WHERE oi.evo_exported = 0
          AND date(o.created_date) BETWEEN date(?) AND date(?)
        """
        params: List[Any] = [from_date, to_date]

        if supplier:
            sql += " AND s.name LIKE ?"
            params.append(f"%{supplier}%")
        if project:
            sql += " AND oi.project = ?"
            params.append(project)
        if q:
            sql += " AND (oi.item_code LIKE ? OR o.order_number LIKE ? OR s.name LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])

        sql += " ORDER BY o.created_date DESC, oi.id DESC LIMIT ?"
        params.append(limit)

        rows = c.execute(sql, params).fetchall()
        if not rows:
            return {"rows": [], "from_date": from_date, "to_date": to_date, "count": 0}

        # Prefill defaults
        out: List[Dict[str, Any]] = []
        for r in rows:
            created_iso = r["created_date"]  # stored as TEXT; assume ISO-ish
            # Ensure ISO for ymd_to_export()
            created_iso = created_iso.replace(" ", "T") if " " in created_iso else created_iso
            export_date = ymd_to_export(created_iso, settings["date_format"])

            description = apply_template(
                settings["description_template"],
                {
                    "order_number": r["order_number"],
                    "supplier_name": r["supplier_name"] or "",
                    "project": r["project"] or "",
                    "date": export_date,
                },
            )

            out.append({
                "order_item_id": r["order_item_id"],
                "item_code": r["item_code"] or "",
                "supplier_name": r["supplier_name"] or "",
                "project": r["project"] or "",
                "order_number": r["order_number"],

                "date": export_date,
                "reference": f"PO-{r['order_number']}",
                "description": description,
                "warehouse_code": settings["default_warehouse_code"],
                "transaction_code": settings["default_transaction_code"],
                "gl_contra_account": settings["default_gl_contra_account"],
                "qty_in": float(r["qty_ordered"] or 0),
                "qty_out": 0.0,
                "new_cost": None,
                "project_code": r["project_code"] or None,
                "job_code": None,
                "lot_number": None,
            })

        return {"rows": out, "from_date": from_date, "to_date": to_date, "count": len(out)}

@router.post("/export")
def export_rows(payload: ExportPayload, current_user: str = "system"):
    """
    Creates a batch, writes CSV, stamps flags on included order_items.
    Skips any rows already flagged (defensive).
    """
    if not payload.rows:
        raise HTTPException(status_code=400, detail="No rows supplied")

    with get_db_connection() as conn:
        c = conn.cursor()
        settings = get_settings(conn)

        # Insert batch shell
        c.execute(
            "INSERT INTO evo_export_batches (created_by, filename, notes, row_count) VALUES (?, ?, ?, 0)",
            (current_user, "", payload.notes or ""),
        )
        batch_id = c.lastrowid

        # Prepare CSV path
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"evo_{batch_id}_{timestamp}.csv"
        full_path = os.path.join(CSV_DIR, filename)

        # Write CSV
        encoding = settings.get("encoding", "utf-8") or "utf-8"
        written = 0
        with open(full_path, "w", newline="", encoding=encoding, errors="ignore") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(CSV_HEADERS)

            for row in payload.rows:
                # Skip if already exported
                exists = c.execute("SELECT evo_exported FROM order_items WHERE id = ?", (row.order_item_id,)).fetchone()
                if not exists:
                    continue
                if int(exists["evo_exported"] or 0) == 1:
                    continue

                csv_row = [
                    row.item_code,
                    row.warehouse_code,
                    row.date,                 # already YYYY/MM/DD
                    row.reference,
                    row.description,
                    row.qty_in,
                    row.qty_out or "",
                    row.new_cost or "",
                    row.transaction_code,
                    row.project_code or "",
                    row.job_code or "",
                    row.gl_contra_account,
                    row.lot_number or "",
                ]
                writer.writerow(csv_row)
                row_hash = sha1_row(csv_row)

                c.execute("""
                    UPDATE order_items
                       SET evo_exported = 1,
                           evo_export_batch_id = ?,
                           evo_exported_at = datetime('now'),
                           evo_export_hash = ?
                     WHERE id = ?
                """, (batch_id, row_hash, row.order_item_id))
                written += 1

        # Update batch row_count + filename
        c.execute("UPDATE evo_export_batches SET row_count = ?, filename = ? WHERE id = ?", (written, filename, batch_id))
        conn.commit()

        if written == 0:
            # Nothing actually written → remove empty CSV file if created
            try:
                if os.path.exists(full_path):
                    os.remove(full_path)
            except Exception:
                pass
            return JSONResponse(status_code=200, content={
                "batch_id": batch_id,
                "filename": None,
                "row_count": 0,
                "download_url": None,
                "message": "No new rows exported (all were already flagged)."
            })

        return {
            "batch_id": batch_id,
            "filename": filename,
            "row_count": written,
            "download_url": f"/evo/batches/{batch_id}/download"
        }

@router.get("/batches")
def list_batches(limit: int = 10):
    with get_db_connection() as conn:
        c = conn.cursor()
        rows = c.execute("""
            SELECT id, created_at, created_by, filename, notes, row_count
              FROM evo_export_batches
             ORDER BY id DESC
             LIMIT ?
        """, (limit,)).fetchall()
        return {"batches": [dict(r) for r in rows]}

@router.get("/batches/{batch_id}/download")
def download_batch(batch_id: int):
    with get_db_connection() as conn:
        c = conn.cursor()
        row = c.execute("SELECT filename FROM evo_export_batches WHERE id = ?", (batch_id,)).fetchone()
        if not row or not row["filename"]:
            raise HTTPException(status_code=404, detail="Batch not found")
        path = os.path.join(CSV_DIR, row["filename"])
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File missing on server")
        return FileResponse(path, filename=row["filename"], media_type="text/csv")

@router.post("/admin/unflag")
def admin_unflag(payload: UnflagPayload):
    if not payload.order_item_ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    with get_db_connection() as conn:
        c = conn.cursor()
        qmarks = ",".join(["?"] * len(payload.order_item_ids))
        c.execute(f"""
            UPDATE order_items
               SET evo_exported = 0,
                   evo_export_batch_id = NULL,
                   evo_exported_at = NULL,
                   evo_export_hash = NULL
             WHERE id IN ({qmarks})
        """, payload.order_item_ids)
        conn.commit()
        return {"updated": c.rowcount}
