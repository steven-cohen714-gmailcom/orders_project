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
        cursor = conn.cursor()

        user = request.session.get("user")
        if not user or "id" not in user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = user["id"]

        # Step 1: Get order details
        cursor.execute("SELECT status, required_auth_band FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        
        current_status = row["status"]
        required_auth_band = row["required_auth_band"]

        # Step 2: Prevent marking if already 'Paid'
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

        # Step 4: Fetch and sum existing payments
        cursor.execute("SELECT amount_paid FROM order_payments WHERE order_id = ?", (order_id,))
        payments = cursor.fetchall()
        total_paid_so_far = sum(p["amount_paid"] for p in payments)

        # Step 5: Process payment data and determine statuses for both tables
        new_amount_paid = payment.amount_paid
        if new_amount_paid <= 0:
            raise HTTPException(status_code=400, detail="Payment amount must be positive")
        
        total_after_payment = total_paid_so_far + new_amount_paid

        # --- REVISED LOGIC START ---
        # Map the user's selection to the correct status for each table
        order_status_for_orders_table = None
        payment_status_for_payments_table = None
        
        if payment.payment_status == "Paid":
            order_status_for_orders_table = "Paid"
            payment_status_for_payments_table = "Fully Paid"
        elif payment.payment_status == "Partially Paid":
            order_status_for_orders_table = "Partially Paid"
            payment_status_for_payments_table = "Not Fully Paid"
        else:
            # Fallback for an invalid status, though frontend should prevent this
            raise HTTPException(status_code=400, detail="Invalid payment status provided.")
        # --- REVISED LOGIC END ---

        # Step 6: Insert into order_payments for history
        cursor.execute("""
            INSERT INTO order_payments (order_id, amount_paid, payment_date, payment_status, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, new_amount_paid, payment.payment_date, payment_status_for_payments_table, user_id, datetime.now().isoformat()))

        # Step 7: Update orders table with cumulative amount and new status
        cursor.execute("""
            UPDATE orders
            SET
                status = ?,
                amount_paid = ?,
                payment_date = ?
            WHERE id = ?
        """, (order_status_for_orders_table, total_after_payment, payment.payment_date, order_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found for update.")

        # Step 8: Audit trail: Log the successful payment
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
            VALUES (?, 'Marked COD Payment', ?, ?, ?)
        """, (
            order_id,
            f"Amount: R{new_amount_paid:.2f}, Date: {payment.payment_date}, New Status: {order_status_for_orders_table}",
            datetime.now().isoformat(), 
            user_id
        ))

        conn.commit() 

        # Log file: Log the successful action
        log_event("cod_payments.log", {
            "order_id": order_id,
            "action": "marked_paid_success",
            "amount_paid": new_amount_paid,
            "total_after_payment": total_after_payment,
            "new_order_status": order_status_for_orders_table,
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
