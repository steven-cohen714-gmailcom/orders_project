# File: backend/endpoints/authorisations_api.py
# Relative Path: backend/endpoints/authorisations_api.py

from fastapi import APIRouter, Request, HTTPException, Query
from backend.database import get_db_connection
from datetime import datetime
import json
import logging
import sqlite3
from typing import Optional

from backend.utils.authorisation_engine import apply_authoriser_action
from backend.utils.email_and_alerts_engine import dispatch
from backend.utils.statuses import AWAITING_AUTHORISATION

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


@router.get("/orders/api/awaiting_authorisation")
async def get_orders_awaiting_authorisation(
    request: Request,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
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
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        filters = []
        params = []

        # Queue shows only orders in the canonical awaiting state
        filters.append("o.status = ?")
        params.append(AWAITING_AUTHORISATION)

        # Visibility rule:
        # - Band 1: see NULL/0/1 (legacy + band 1)
        # - Band >=2: see anything up to your band (<=)
        # (This matches "emails go to user_band >= required_band")
        try:
            band = int(band)
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid user band")

        filters.append(
            """
        (
          (? = 1 AND (o.required_auth_band IS NULL OR o.required_auth_band = 0 OR o.required_auth_band = 1))
          OR
          (? >= 2 AND o.required_auth_band <= ?)
        )
        """
        )
        params.extend([band, band, band])

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
            ORDER BY datetime(o.created_date) DESC, o.id DESC
        """
        logger.info(f"Executing {AWAITING_AUTHORISATION} query: {query} with params: {params}")
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except Exception as e:
        logger.error(f"Error fetching orders awaiting authorisation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders for authorisation: {e}")
    finally:
        conn.close()


@router.post("/orders/api/authorise_order/{order_id}")
async def authorise_order(order_id: int, request: Request):
    """
    Authoriser → delegate to authorisation_engine, then persist and dispatch emails.
    """
    raw = request.session.get("user")
    try:
        user = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session format")
    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")

    user_id = user.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Session missing user id")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Ensure order exists and is awaiting authorisation
        cursor.execute("SELECT id, order_number, status FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        if (row["status"] or "").strip() != AWAITING_AUTHORISATION:
            raise HTTPException(
                status_code=400,
                detail=f"Order not awaiting authorisation (current: {row['status']})",
            )

        # 1) Compute decision (approve)
        result = apply_authoriser_action(order_id=order_id, action="approve", actor_user_id=user_id)

        # 2) Persist new status (keep required_auth_band as-is)
        cursor.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (result.new_status, order_id),
        )

        # 3) Audit rows
        when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for details in result.audit_rows:
            cursor.execute(
                "INSERT INTO audit_trail (order_id, action, details, user_id, action_date) VALUES (?, ?, ?, ?, ?)",
                (order_id, "Authorisation", details, user_id, when),
            )

        conn.commit()

        # 4) Send emails (COD-ready, etc.)
        dispatch(result.email_triggers)

        return {"message": f"Order {row['order_number']} → {result.new_status}"}

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"Authorise failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Authorise failed: {e}")
    finally:
        conn.close()
