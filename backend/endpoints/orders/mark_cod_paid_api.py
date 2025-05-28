# File: backend/endpoints/orders/mark_cod_paid_api.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from backend.database import get_db_connection
from datetime import datetime

router = APIRouter()

class PaymentInfo(BaseModel):
    order_id: int
    payment_date: str  # YYYY-MM-DD
    amount_paid: float

@router.post("/orders/api/mark_cod_paid")
def mark_cod_paid(payload: PaymentInfo, request: Request):
    try:
        user = request.session.get("user", "unknown")
        order_id = payload.order_id
        payment_date = payload.payment_date
        amount_paid = payload.amount_paid

        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE orders
                SET payment_date = ?, amount_paid = ?
                WHERE id = ?
            """, (payment_date, amount_paid, order_id))

            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, user_id)
                VALUES (?, 'Payment Recorded', ?, ?)
            """, (
                order_id,
                f"Payment recorded: R{amount_paid:,.2f} on {payment_date}",
                user
            ))

            conn.commit()

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record payment: {str(e)}")
