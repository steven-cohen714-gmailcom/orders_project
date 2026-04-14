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
    payment_status: str  # The user's choice: "Paid" or "Partially Paid"

def log_event(filename: str, data: dict):
    """Logs an event to a file, used for general logs not audit trail."""
    log_path = Path("logs") / filename
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.put("/orders/mark_cod_paid/{order_id}")
def mark_cod_paid(order_id: int, payment: CodPayment, request: Request):
    conn = None 
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        user = request.session.get("user")
        if not user or "id" not in user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = user["id"]
        # Step 1: Get order details (+ enforce COD eligibility)
        cursor.execute("SELECT status, required_auth_band, payment_terms FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

        current_status = (row["status"] or "").strip()
        required_auth_band = row["required_auth_band"]
        terms_up = (row["payment_terms"] or "").strip().upper()

        # Must be COD, and only payable when status is one of: Pending, Authorised, Partially Paid
        allowed_statuses = {"PENDING", "AUTHORISED", "PARTIALLY PAID"}
        if terms_up != "COD" or current_status.strip().upper() not in allowed_statuses:
            raise HTTPException(status_code=409, detail="Order not eligible for COD payment")

        # Step 2: Enforce authorization if required (over-threshold must be Authorised)
        if required_auth_band is not None and required_auth_band > 0:
            if current_status.strip().upper() != "AUTHORISED":
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

        # Step 3: Fetch and sum existing payments
        cursor.execute("SELECT amount_paid FROM order_payments WHERE order_id = ?", (order_id,))
        payments = cursor.fetchall()
        total_paid_so_far = sum(p["amount_paid"] for p in payments)

        # Step 4: Validate amount and compute new total
        new_amount_paid = float(payment.amount_paid)
        if new_amount_paid <= 0:
            raise HTTPException(status_code=400, detail="Payment amount must be positive")
        total_after_payment = total_paid_so_far + new_amount_paid

        # Step 5: Insert into order_payments (history only)
        # Normalize payment_status for the payments table; keep semantic but do NOT touch orders.status here.
        pay_status = "Fully Paid" if (str(payment.payment_status).strip() == "Paid") else "Not Fully Paid"
        cursor.execute("""
            INSERT INTO order_payments (order_id, amount_paid, payment_date, payment_status, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, new_amount_paid, payment.payment_date, pay_status, user_id, datetime.now().isoformat()))

        # Step 6: Update orders: only cumulative amount + payment_date (NO status change)
        cursor.execute("""
            UPDATE orders
            SET amount_paid = ?, payment_date = ?
            WHERE id = ?
        """, (total_after_payment, payment.payment_date, order_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found for update.")

        # Step 7: Audit trail
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
            VALUES (?, 'COD Payment recorded', ?, ?, ?)
        """, (
            order_id,
            f"Amount: R{new_amount_paid:.2f}, Date: {payment.payment_date}",
            datetime.now().isoformat(),
            user_id
        ))

        conn.commit()

        # Log file: success record (status intentionally unchanged here)
        log_event("cod_payments.log", {
            "order_id": order_id,
            "action": "marked_paid_success",
            "amount_paid": new_amount_paid,
            "total_after_payment": total_after_payment,
            "current_order_status": current_status,
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
