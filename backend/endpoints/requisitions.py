from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3
from pathlib import Path
import traceback

from frontend.static.js.new_requisitions_pdf_generator import generate_requisition_pdf

router = APIRouter(tags=["requisitions"])

DB_PATH = Path("data/orders.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- Models ---------------- #

class RequisitionItem(BaseModel):
    description: str
    quantity: float

class RequisitionPayload(BaseModel):
    requisition_number: str
    requisitioner_id: int
    requisition_note: str
    items: List[RequisitionItem]

# ---------------- Endpoint ---------------- #

@router.post("/requisitions", response_model=dict)
async def submit_requisition(payload: RequisitionPayload):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Step 1: check if requisition_number already exists
            cursor.execute(
                "SELECT 1 FROM requisitions WHERE requisition_number = ?",
                (payload.requisition_number,)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Requisition number already exists")

            # Step 2: insert new requisition
            cursor.execute("""
                INSERT INTO requisitions (
                    requisition_number,
                    requisitioner_id,
                    requisition_note,
                    requisition_date,
                    status
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                payload.requisition_number,
                payload.requisitioner_id,
                payload.requisition_note,
                datetime.now().isoformat(),
                "submitted"
            ))

            requisition_id = cursor.lastrowid

            for item in payload.items:
                cursor.execute("""
                    INSERT INTO requisition_items (
                        requisition_id,
                        description,
                        quantity
                    ) VALUES (?, ?, ?)
                """, (
                    requisition_id,
                    item.description,
                    item.quantity
                ))

            # Step 3: update settings to bump requisition_number_start
            prefix = ''.join(filter(str.isalpha, payload.requisition_number))
            number = int(''.join(filter(str.isdigit, payload.requisition_number)))
            next_number = f"{prefix}{number + 1}"

            cursor.execute("""
                UPDATE settings
                SET requisition_number_start = ?
            """, (next_number,))

            # ✅ Step 4: relink temporary attachments
            cursor.execute("""
                UPDATE attachments
                SET requisition_id = ?, requisition_number = NULL
                WHERE requisition_id IS NULL AND requisition_number = ?
            """, (
                requisition_id,
                payload.requisition_number
            ))

            conn.commit()
            return {"status": "success", "requisition_id": requisition_id}

    except HTTPException as he:
        raise he  # Preserve intentional 400 errors
    except Exception as e:
        print("🔥 Backend crash:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error submitting requisition: {str(e)}")

@router.get("/api/pending_requisitions", response_model=dict)
def get_pending_requisitions():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.id,
                    r.requisition_number,
                    r.requisition_date,
                    r.requisition_note,
                    r.status,
                    rq.name AS requisitioner,
                    (
                        SELECT GROUP_CONCAT(ri.description, ', ')
                        FROM requisition_items ri
                        WHERE ri.requisition_id = r.id
                    ) AS description,
                    (
                        SELECT SUM(ri.quantity)
                        FROM requisition_items ri
                        WHERE ri.requisition_id = r.id
                    ) AS total_quantity,
                    r.converted_order_id
                FROM requisitions r
                LEFT JOIN requisitioners rq ON r.requisitioner_id = rq.id
                WHERE r.status = 'submitted'
                ORDER BY r.requisition_date DESC
            """)

            rows = cursor.fetchall()
            requisitions = [dict(row) for row in rows]
            return {"requisitions": requisitions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching requisitions: {str(e)}")

@router.get("/api/requisition_items/{requisition_id}")
def get_requisition_items(requisition_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    id,
                    description AS item_description,
                    quantity AS qty_ordered,
                    '-' AS item_code,
                    '-' AS project,
                    0 AS price,
                    0 AS total
                FROM requisition_items
                WHERE requisition_id = ?
            """, (requisition_id,))
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch requisition items: {str(e)}")

@router.get("/requisitions/api/generate_pdf/{requisition_id}")
def requisition_pdf(requisition_id: int):
    try:
        pdf_path = generate_requisition_pdf(requisition_id)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"Requisition_{requisition_id}.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
    
@router.put("/requisitions/api/mark_converted/{requisition_id}") 
def mark_requisition_converted(requisition_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Safety: check if requisition exists
            cursor.execute("SELECT id FROM requisitions WHERE id = ?", (requisition_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Requisition not found")

            # Update with dummy order ID (just mark it as converted)
            cursor.execute("""
                UPDATE requisitions
                SET converted_order_id = 'ORDER-CONVERTED'
                WHERE id = ?
            """, (requisition_id,))
            conn.commit()

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark converted: {str(e)}")

