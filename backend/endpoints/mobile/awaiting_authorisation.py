from fastapi import APIRouter, Request, HTTPException
from backend.database import get_db_connection
from datetime import datetime
import json

router = APIRouter()

@router.get("/orders/api/awaiting_authorisation")
async def get_orders_awaiting_authorisation(request: Request):
    raw = request.session.get("user")
    try:
        user = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session format")

    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")

    band = user.get("auth_threshold_band")
    if band is None:
        raise HTTPException(status_code=403, detail="User does not have an authorisation band")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, order_number, total, created_date
            FROM orders
            WHERE status = 'Awaiting Authorisation'
            AND required_auth_band = ?
            ORDER BY created_date DESC
        """, (band,))
        return [dict(row) for row in cursor.fetchall()]


@router.post("/orders/api/authorise_order/{order_id}")
async def authorise_order(order_id: int, request: Request):
    raw = request.session.get("user")
    try:
        user = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session format")

    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")

    username = user.get("username")
    user_id = user.get("id")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Check if order exists and is still awaiting authorisation
        cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        if row["status"] != "Awaiting Authorisation":
            raise HTTPException(status_code=400, detail="Order is not in an authorisable state")

        # Update order status
        cursor.execute("""
            UPDATE orders
            SET status = 'Authorised'
            WHERE id = ?
        """, (order_id,))

        # Insert into audit trail
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
            VALUES (?, 'Authorised', ?, ?, ?)
        """, (
            order_id,
            f"Order authorised by {username}",
            datetime.utcnow().isoformat(),
            user_id
        ))

        conn.commit()
        return {"status": "success", "message": "Order authorised"}
