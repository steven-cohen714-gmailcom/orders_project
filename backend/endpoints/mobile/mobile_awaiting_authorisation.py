# File: backend/endpoints/mobile/mobile_awaiting_authorisation.py

from fastapi import APIRouter, Request, HTTPException, Query, Depends
from backend.database import get_db_connection
from datetime import datetime
from fastapi.responses import JSONResponse
import json
import logging
from typing import Optional, Dict

router = APIRouter()
logger = logging.getLogger("uvicorn")

# Helper function (copied from order_queries.py to be self-contained)
def validate_date(date_str: Optional[str]) -> Optional[str]:
    """Helper function to validate date strings."""
    if not date_str:
        return None
    try:
        dt_obj = None
        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            try:
                dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    dt_obj = datetime.strptime(date_str, "%Y/%m/%d")
        if dt_obj:
            return dt_obj.strftime("%Y-%m-%d")
        return None
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


@router.get("/mobile/get_user_info")
async def get_user_info(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    logger.info(f"🔍 Session user before JSONResponse: {user}")
    return JSONResponse(content=user if isinstance(user, dict) else json.loads(user))


@router.get("/orders/api/awaiting_authorisation")
async def get_orders_awaiting_authorisation(
    request: Request,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None)
):
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

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        filters = []
        params = []

        filters.append("o.status = 'Awaiting Authorisation'")

        # MODIFIED: Logic for required_auth_band based on user's band to include Band 5
        if band == 1:
            # Band 1 can authorize orders requiring band 1, or those with no/zero required band
            filters.append("(o.required_auth_band = ? OR o.required_auth_band IS NULL OR o.required_auth_band = 0)")
            params.append(band)
        elif band == 5:
            # Band 5 can authorize orders requiring Band 5
            filters.append("o.required_auth_band = ?")
            params.append(band)
        else:
            # Other bands (2, 3, 4) can only authorize orders specifically requiring their band
            filters.append("o.required_auth_band = ?")
            params.append(band)

        # Apply additional filters (start_date, end_date, requester, supplier)
        if start_date:
            valid_start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(valid_start_date)

        if end_date:
            valid_end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(valid_end_date)

        if requester is not None and requester.strip().lower() != "all" and requester.strip() != "":
            filters.append("UPPER(r.name) LIKE UPPER(?)")
            params.append(f"%{requester.strip()}%")

        if supplier is not None and supplier.strip().lower() != "all" and supplier.strip() != "":
            filters.append("UPPER(s.name) LIKE UPPER(?)")
            params.append(f"%{supplier.strip()}%")
        
        where_clause = " AND ".join(filters) if filters else "1=1"

        query = f"""
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
            WHERE {where_clause}
            ORDER BY o.created_date DESC
        """
        
        logger.info(f"Executing Awaiting Authorisation Query: {query} with params: {params}")
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error fetching orders awaiting authorisation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders for authorisation: {e}")
    finally:
        conn.close()


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
            WHERE id = ?
            AND status = 'Awaiting Authorisation'
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

        conn.commit()

    return {"message": "Order authorised"}