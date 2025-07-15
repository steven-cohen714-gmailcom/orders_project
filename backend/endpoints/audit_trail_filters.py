# File: backend/endpoints/audit_trail_filters.py

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List, Dict
from datetime import datetime
import sqlite3
from pathlib import Path
import json

from backend.database import get_db_connection
from backend.utils.permissions_utils import require_login

router = APIRouter()

def log_event(filename: str, data: dict):
    """Logs an event to a file."""
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

def validate_date(date_str: Optional[str]) -> Optional[str]:
    """Helper function to validate date strings."""
    if not date_str:
        return None
    try:
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return dt_obj.strftime("%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


@router.get("/audit_trail_orders") # CHANGED: Now simply "/audit_trail_orders"
async def get_audit_trail_filtered_data(
    status: Optional[str] = Query(None, description="Filter by order status"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    user: Dict = Depends(require_login)
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters = []
        params = []

        if status and status.lower() != "all":
            filters.append("UPPER(o.status) = UPPER(?)")
            params.append(status)

        if start_date:
            valid_start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(valid_start_date)

        if end_date:
            valid_end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(valid_end_date)

        if requester and requester.lower() != "all":
            filters.append("UPPER(r.name) LIKE UPPER(?)")
            params.append(f"%{requester}%")

        if supplier and supplier.lower() != "all":
            filters.append("UPPER(s.name) LIKE UPPER(?)")
            params.append(f"%{supplier}%")

        where_clause = " AND ".join(filters) if filters else "1=1"

        cursor = conn.execute(f"""
            SELECT
                o.id, o.created_date, o.received_date, o.order_number,
                r.name AS requester, s.name AS supplier,
                o.order_note, o.note_to_supplier, o.total, o.status,
                u.username AS audit_user
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN (
                SELECT
                    at.order_id,
                    at.user_id,
                    MAX(at.action_date) AS latest_action_date
                FROM audit_trail at
                GROUP BY at.order_id
            ) AS latest_audit ON latest_audit.order_id = o.id
            LEFT JOIN users u ON latest_audit.user_id = u.id
            WHERE {where_clause}
            ORDER BY o.created_date DESC, o.order_number DESC
        """, params)

        orders = [dict(row) for row in cursor.fetchall()]

        for order in orders:
            if order["created_date"]:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                order["created_date"] = "N/A"

            if order["received_date"]:
                try:
                    order["received_date"] = datetime.strptime(order["received_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    order["received_date"] = datetime.strptime(order["received_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                order["received_date"] = "N/A"
        
        log_event("audit_trail_log.txt", {
            "action": "fetch_audit_trail_orders_filtered",
            "count": len(orders),
            "filters": {"status": status, "start_date": start_date, "end_date": end_date, "requester": requester, "supplier": supplier}
        })
        return {"orders": orders}

    except Exception as e:
        log_event("audit_trail_log.txt", {"error": str(e), "type": "audit_trail_orders_filtered"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail orders: {e}")
    finally:
        conn.close()