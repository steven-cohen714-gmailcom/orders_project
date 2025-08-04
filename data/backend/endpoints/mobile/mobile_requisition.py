# File: backend/endpoints/mobile/mobile_requisition.py

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime
from backend.database import get_db_connection, get_next_requisition_number

router = APIRouter(prefix="/mobile_requisition", tags=["mobile requisition"])

class RequisitionPayload(BaseModel):
    description: str
    quantity: float
    note: str | None = None

@router.post("/submit")
async def submit_requisition(request: Request, payload: RequisitionPayload):
    session = request.session
    requisitioner_id = session.get("requisitioner_id")

    if not requisitioner_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    if not payload.description or payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid data")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            requisition_number = get_next_requisition_number()

            # Insert master record
            cursor.execute("""
                INSERT INTO requisitions (
                    requisition_number, requisitioner_id, requisition_note, requisition_date
                ) VALUES (?, ?, ?, ?)
            """, (
                requisition_number,
                requisitioner_id,
                payload.note or "",
                datetime.now().isoformat()
            ))
            requisition_id = cursor.lastrowid

            # Insert line item
            cursor.execute("""
                INSERT INTO requisition_items (
                    requisition_id, description, quantity
                ) VALUES (?, ?, ?)
            """, (requisition_id, payload.description, payload.quantity))

            conn.commit()

        return {"message": "Requisition submitted", "requisition_number": requisition_number}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving requisition: {e}")
