from fastapi import APIRouter, Request, HTTPException
from backend.database import get_db_connection
from datetime import datetime
from fastapi.responses import JSONResponse
import json
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.get("/mobile/get_user_info")
async def get_user_info(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    logger.info(f"🔍 Session user before JSONResponse: {user}")
    return JSONResponse(content=user if isinstance(user, dict) else json.loads(user))


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
            SELECT 
                o.id,
                o.order_number,
                o.total,
                o.created_date,
                o.status,
                o.required_auth_band,
                o.order_note,
                r.name AS requester_name,
                s.name AS supplier_name
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            WHERE o.status = 'Awaiting Authorisation'
              AND o.required_auth_band = ?
            ORDER BY o.created_date DESC
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

        # Update order status safely
        cursor.execute("""
            UPDATE orders
            SET status = 'Authorised'
            WHERE id = ? AND status = 'Awaiting Authorisation'
        """, (order_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=400, detail="Order was already authorised or in an invalid state")

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

        conn.commit()  # ✅ ensure commit happens before connection closes

    return {"message": "Order authorised"}
