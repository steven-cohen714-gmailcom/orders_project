from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3
from pathlib import Path

router = APIRouter(tags=["requisitions"])

DB_PATH = Path("data/orders.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- Models ---------------- #

class RequisitionItem(BaseModel):
    description: str
    project: str
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

            # Insert into requisitions table
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

            # Insert each line item
            for item in payload.items:
                cursor.execute("""
                    INSERT INTO requisition_items (
                        requisition_id,
                        description,
                        project,
                        quantity
                    ) VALUES (?, ?, ?, ?)
                """, (
                    requisition_id,
                    item.description,
                    item.project,
                    item.quantity
                ))

            conn.commit()
            return {"status": "success", "requisition_id": requisition_id}

    except Exception as e:
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
                        SELECT GROUP_CONCAT(ri.project, ', ')
                        FROM requisition_items ri
                        WHERE ri.requisition_id = r.id
                    ) AS project,
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
