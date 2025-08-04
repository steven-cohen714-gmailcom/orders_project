# File: backend/endpoints/lookups/mark_cod_paid_api.py

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection
from datetime import datetime
from pathlib import Path
import json
import sqlite3

router = APIRouter()

class CodPayment(BaseModel):
    amount_paid: float
    payment_date: str  # Format: YYYY-MM-DD

def log_event(filename: str, data: dict):
    """Logs an event to a file, used for general logs not audit trail."""
    log_path = Path("logs") / filename
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.put("/mark_cod_paid/{order_id}")
def mark_cod_paid(order_id: int, payment: CodPayment, request: Request):
    conn = None 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        user = request.session.get("user")
        if not user or "id" not in user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = user["id"]

        # Step 1: Get current status and required_auth_band
        cursor.execute("SELECT status, required_auth_band FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        
        current_status = row["status"]
        required_auth_band = row["required_auth_band"]

        # Step 2: Prevent marking as paid if already 'Paid'
        if current_status == "Paid":
            log_event("cod_payments.log", {
                "order_id": order_id,
                "action": "attempt_duplicate_payment",
                "message": "Order already marked as Paid",
                "status": current_status,
                "user_id": user_id
            })
            raise HTTPException(status_code=400, detail="Order is already marked as Paid")

        # Step 3: Enforce authorization if required
        # If required_auth_band is not NULL and not 0, it means authorization is needed.
        # In such cases, the status *must* be 'Authorised' to proceed with payment.
        if required_auth_band is not None and required_auth_band > 0:
            if current_status != "Authorised":
                log_event("cod_payments.log", {
                    "order_id": order_id,
                    "action": "attempt_pay_unauthorised_order",
                    "message": "Order requires authorization but is not yet Authorised",
                    "status": current_status,
                    "required_auth_band": required_auth_band,
                    "user_id": user_id
                })
                raise HTTPException(
                    status_code=403, 
                    detail=f"Order status must be 'Authorised' to mark payment. Current status: '{current_status}'."
                )

        # Step 4: Update COD payment info and status
        cursor.execute("""
            UPDATE orders
            SET
                status = 'Paid',
                amount_paid = ?,
                payment_date = ?
            WHERE id = ?
        """, (payment.amount_paid, payment.payment_date, order_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found for update.")

        # Step 5: Audit trail: Log the successful payment
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
            VALUES (?, 'Marked COD Paid', ?, ?, ?)
        """, (
            order_id,
            f"Amount: R{payment.amount_paid:.2f}, Date: {payment.payment_date}",
            datetime.now().isoformat(), 
            user_id
        ))

        conn.commit() 

        # Log file: Log the successful action
        log_event("cod_payments.log", {
            "order_id": order_id,
            "action": "marked_paid_success",
            "amount_paid": payment.amount_paid,
            "payment_date": payment.payment_date,
            "marked_by_user_id": user_id
        })

        return {"success": True}

    except HTTPException as http_exc:
        if conn:
            conn.rollback() 
        raise http_exc
    except sqlite3.Error as db_err:
        if conn:
            conn.rollback() 
        log_event("cod_payments.log", {"error": str(db_err), "type": "sqlite_error", "order_id": order_id})
        raise HTTPException(status_code=500, detail=f"Database error saving payment: {str(db_err)}")
    except Exception as e:
        if conn:
            conn.rollback() 
        log_event("cod_payments.log", {"error": str(e), "type": "general_error", "order_id": order_id})
        raise HTTPException(status_code=500, detail=f"Failed to save COD payment: {str(e)}")
    finally:
        if conn:
            conn.close()