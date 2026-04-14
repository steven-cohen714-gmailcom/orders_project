# File: backend/endpoints/review_orders.py

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from backend.database import get_db_connection
from backend.utils.authorisation_engine import apply_review_decision
from backend.utils.email_and_alerts_engine import dispatch
from backend.utils.statuses import FOR_REVIEW, ON_HOLD
from backend.utils.permissions_utils import require_login, require_screen_permission
from backend.utils.time_utils import now_utc_iso
import sqlite3
import io
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

router = APIRouter()

# IMPORTANT:
# main.py includes this router with: app.include_router(review_orders.router, prefix="/orders")
# So paths here must start with "/api/..." (NOT "/orders/api/..."), yielding "/orders/api/...".

@router.get("/api/review_orders")
def get_review_orders(
    start_date: str = None,
    end_date: str = None,
    requester: str = None,
    supplier: str = None,
):
    """
    Returns orders with status 'For Review' or 'On Hold'. Optional filters by date/requester/supplier.
    Dates from <input type="date"> come as 'YYYY-MM-DD' — we widen to whole-day ranges.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.id, o.order_number, o.created_date, o.total, o.status,
               r.name AS requester, s.name AS supplier, o.order_note
        FROM orders o
        LEFT JOIN requesters r ON o.requester_id = r.id
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        WHERE o.status IN (?, ?)
    """
    params = [FOR_REVIEW, ON_HOLD]

    if start_date:
        query += " AND o.created_date >= ?"
        params.append(f"{start_date} 00:00:00")
    if end_date:
        query += " AND o.created_date <= ?"
        params.append(f"{end_date} 23:59:59")
    if requester and requester != "All":
        query += " AND r.name = ?"
        params.append(requester)
    if supplier and supplier != "All":
        query += " AND s.name = ?"
        params.append(supplier)

    query += " ORDER BY o.created_date DESC, o.id DESC"

    cursor.execute(query, params)
    colnames = [c[0] for c in cursor.description]
    orders = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    conn.close()
    return {"orders": orders}

@router.post("/api/mark_reviewed/{order_id}")
async def mark_order_reviewed(
    order_id: int,
    request: Request,
    _: bool = Depends(require_login),  # gate only; read user from session
):
    """
    Review → delegate to authorisation_engine, then persist and dispatch emails.
    """
    # get user id from session (robust to string/dict session formats)
    raw = request.session.get("user")
    try:
        user = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        user = {}
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Ensure order exists and is eligible
        cursor.execute("SELECT id, order_number, status FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        current_status = (row["status"] or "").strip()
        if current_status not in (FOR_REVIEW, ON_HOLD):
            raise HTTPException(status_code=400, detail=f"Order not eligible for Review (current: {current_status})")

        # 1) Compute decision
        result = apply_review_decision(order_id=order_id, action="reviewed", actor_user_id=user_id)

        # 2) Persist status + required_band
        cursor.execute(
            "UPDATE orders SET status = ?, required_auth_band = ? WHERE id = ?",
            (result.new_status, result.required_auth_band, order_id),
        )

        # 3) Audit rows
        when = now_utc_iso()
        for details in result.audit_rows:
            cursor.execute(
                "INSERT INTO audit_trail (order_id, action, details, user_id, action_date) VALUES (?, ?, ?, ?, ?)",
                (order_id, "Reviewed", details, user_id, when),
            )

        conn.commit()

        # 4) Send emails (idempotent inside engine)
        dispatch(result.email_triggers)

        return {
            "message": f"Order {row['order_number']} reviewed → '{result.new_status}'",
            "status": result.new_status,
            "required_band": result.required_auth_band,
        }

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Mark reviewed failed: {e}")
    finally:
        conn.close()

@router.post("/api/mark_on_hold/{order_id}")
async def mark_on_hold(
    order_id: int,
    request: Request,
    _: bool = Depends(require_login),  # gate only; read user from session
):
    # get user id from session
    raw = request.session.get("user")
    try:
        user = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        user = {}
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, order_number, status FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

        current_status = (row["status"] or "").strip()
        if current_status not in (FOR_REVIEW, ON_HOLD):
            raise HTTPException(status_code=400, detail=f"Order not eligible for On Hold (current: {current_status})")

        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (ON_HOLD, order_id))
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
            VALUES (?, 'On Hold', 'Reviewer set status to On Hold', ?, ?)
        """, (order_id, user_id, now_utc_iso()))

        conn.commit()
        return {"message": f"Order {row['order_number']} set to 'On Hold'."}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Mark on hold failed: {e}")
    finally:
        conn.close()

@router.post("/api/convert_on_hold_to_draft/{order_id}")
async def convert_on_hold_to_draft(
    order_id: int,
    request: Request,
    _: bool = Depends(require_login),  # gate only; read user from session
    __: bool = Depends(require_screen_permission("review_orders")),  # must have review permission
):

    """
    Convert an order in 'On Hold' back to a Draft so it can be edited.
    - Preserves the SAME order_number
    - Copies header + items into draft tables
    - Deletes the original items and marks the original order as 'Deleted' (avoid duplicates; keep provenance)
    - Lands the user in Drafts flow on the frontend
    Returns: { draft_id, order_number }
    """
    # get user id from session (robust to string/dict session formats)
    raw = request.session.get("user")
    try:
        user = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        user = {}
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # --- 1) Verify order exists and is On Hold ---
        cursor.execute("""
            SELECT id, order_number, status, order_note, note_to_supplier, supplier_id,
                   requester_id, payment_terms, total
            FROM orders
            WHERE id = ?
        """, (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

        current_status = (row["status"] or "").strip()
        if current_status != ON_HOLD:
            raise HTTPException(status_code=400, detail=f"Only 'On Hold' orders can be converted to Draft (current: {current_status})")

        order_number = row["order_number"]

        # --- 2) Start transaction ---
        # (sqlite3 in Python starts a txn automatically on first write; we still treat it as a unit)
        # Copy header into draft_orders (preserve SAME order_number)

        cursor.execute("""
            INSERT INTO draft_orders (
                order_number,
                status,
                created_date,
                total,
                order_note,
                note_to_supplier,
                supplier_id,
                requester_id,
                payment_terms,
                last_modified_by_user_id
            )
            VALUES (?, 'Draft', ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_number,
            now_utc_iso(),  # UTC ISO timestamp
            row["total"],
            row["order_note"],
            row["note_to_supplier"],
            row["supplier_id"],
            row["requester_id"],
            row["payment_terms"],
            user_id,
        ))

        draft_id = cursor.lastrowid

        # --- 3) Copy items into draft_order_items ---
        cursor.execute("""
            SELECT item_code, item_description, project, qty_ordered, price, total
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        items = cursor.fetchall()

        if items:
            cursor.executemany("""
                INSERT INTO draft_order_items (
                    draft_order_id,
                    item_code,
                    item_description,
                    project,
                    qty_ordered,
                    price,
                    total
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    draft_id,
                    it["item_code"],
                    it["item_description"],
                    it["project"],
                    it["qty_ordered"],
                    it["price"],
                    it["total"],
                )
                for it in items
            ])

        # --- 4) Audit trail on the original order (will remain even after deletion) ---
        when = now_utc_iso()
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
            VALUES (?, 'Converted to Draft', ?, ?, ?)
        """, (order_id, f"Converted to Draft draft_id={draft_id}", user_id, when))

        # --- 5) Remove original items, and mark the original order as Deleted ---
        # Items are removed to prevent duplication in item-level reports; header remains for provenance.
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cursor.execute("UPDATE orders SET status = 'Deleted' WHERE id = ?", (order_id,))


        # --- 6) Commit ---
        conn.commit()

        return {
            "draft_id": draft_id,
            "order_number": order_number,
            "message": f"Order {order_number} converted to Draft (draft_id={draft_id})"
        }

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Convert to draft failed: {e}")
    finally:
        conn.close()

@router.get("/api/generate_pdf_with_projects/{order_id}")
def generate_pdf_with_projects(order_id: int):
    """
    INTERNAL PDF (includes project code + project name).
    Matches your schema: order_items.project (text) joins projects.project_code.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.order_number, o.created_date, r.name AS requester, s.name AS supplier
        FROM orders o
        LEFT JOIN requesters r ON o.requester_id = r.id
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        WHERE o.id = ?
    """, (order_id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    cursor.execute("""
        SELECT
            oi.item_code,
            oi.item_description,
            oi.qty_ordered,
            oi.price,
            oi.project AS project_code,
            p.project_name
        FROM order_items oi
        LEFT JOIN projects p ON p.project_code = oi.project
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    order_number, created_date, requester_name, supplier_name = order[0], order[1], order[2], order[3]

    elements.append(Paragraph(f"Order Number: {order_number}", styles["Title"]))
    elements.append(Paragraph(f"Date: {created_date}", styles["Normal"]))
    elements.append(Paragraph(f"Requester: {requester_name}", styles["Normal"]))
    elements.append(Paragraph(f"Supplier: {supplier_name}", styles["Normal"]))
    elements.append(Spacer(1, 8))

    from reportlab.lib.styles import ParagraphStyle  # add at top if not present

    # Header as Paragraphs so they wrap/measure correctly
    header = ParagraphStyle(
        "th", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=9, leading=11,
        textColor=colors.whitesmoke, alignment=1  # center
    )
    wrap = ParagraphStyle("wrap", parent=styles["Normal"], fontSize=9, leading=11, wordWrap="CJK")

    data = [[
        Paragraph("Code", header),
        Paragraph("Description", header),
        Paragraph("Qty", header),
        Paragraph("Unit Price", header),
        Paragraph("Project Code", header),
        Paragraph("Project Name", header),
    ]]

    for item in items:
        item_code, item_desc, qty, unit_price, proj_code, proj_name = item
        data.append([
            item_code or "",
            Paragraph(item_desc or "", wrap),
            "" if qty is None else str(qty),
            f"R{(unit_price or 0):.2f}",
            proj_code or "",
            Paragraph(proj_name or "", wrap),
        ])

    # keep the total width = doc.width so nothing gets cut off
    col_widths = [
    doc.width * 0.12,  # Code
    doc.width * 0.31,  # Description
    doc.width * 0.08,  # Qty
    doc.width * 0.13,  # Unit Price
    doc.width * 0.12,  # Project Code (wider)
    doc.width * 0.24,  # Project Name
]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.whitesmoke),

    ("ALIGN",      (0, 0), (-1, 0), "CENTER"),  # header
    ("VALIGN",     (0, 0), (-1, 0), "MIDDLE"),  # header

    ("ALIGN",      (0, 1), (-1, -1), "LEFT"),   # body
    ("VALIGN",     (0, 1), (-1, -1), "TOP"),

    ("GRID",       (0, 0), (-1, -1), 0.5, colors.black),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ("TOPPADDING",    (0, 1), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    filename = f"order_{order_number or order_id}_with_projects.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )
