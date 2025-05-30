# File: backend/endpoints/lookups/mark_cod_paid_api.py

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection
from datetime import datetime
from pathlib import Path
import json

router = APIRouter()

class CodPayment(BaseModel):
    amount_paid: float
    payment_date: str  # Format: YYYY-MM-DD

def log_event(filename: str, data: dict):
    log_path = Path("logs") / filename
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.put("/mark_cod_paid/{order_id}")
def mark_cod_paid(order_id: int, payment: CodPayment, request: Request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        user = request.session.get("user")
        if not user or "id" not in user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = user["id"]

        # Check current status before allowing payment
        cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        if row["status"] == "Paid":
            raise HTTPException(status_code=400, detail="Order is already marked as Paid")

        # Update COD payment info
        cursor.execute("""
            UPDATE orders
            SET
                status = 'Paid',
                amount_paid = ?,
                payment_date = ?
            WHERE id = ?
        """, (payment.amount_paid, payment.payment_date, order_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")

        # Audit trail
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id)
            VALUES (?, 'Marked COD as Paid', ?, ?)
        """, (
            order_id,
            f"Amount: R{payment.amount_paid:.2f}, Date: {payment.payment_date}",
            user_id
        ))

        conn.commit()
        conn.close()

        # Log file
        log_event("cod_payments.log", {
            "order_id": order_id,
            "amount_paid": payment.amount_paid,
            "payment_date": payment.payment_date,
            "marked_by_user_id": user_id
        })

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
