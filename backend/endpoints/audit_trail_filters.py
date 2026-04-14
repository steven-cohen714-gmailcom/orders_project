# File: backend/endpoints/audit_trail_filters.py

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List, Dict
from datetime import datetime
import sqlite3
from pathlib import Path
import json

from backend.database import get_db_connection
from backend.utils.permissions_utils import require_login
# Import validate_date from order_queries to reuse its logic
from backend.endpoints.order_queries import validate_date 

router = APIRouter()

def log_event(filename: str, data: dict):
    """Logs an event to a file."""
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

# NOTE: validate_date is now imported from order_queries,
# so this local definition is removed to avoid duplication.
# def validate_date(date_str: Optional[str]) -> Optional[str]:
#     """Helper function to validate date strings."""
#     if not date_str:
#         return None
#     try:
#         dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
#         return dt_obj.strftime("%Y-%m-%d")
#     except ValueError:
#         raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


@router.get("/orders/api/audit_trail_orders") 
async def get_audit_trail_filtered_data(
    status: Optional[str] = Query(None, description="Filter by order status"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    order_number: Optional[str] = Query(None, description="Filter by a specific order number"),
    user: Dict = Depends(require_login) # Assuming require_login is still desired here
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters = []
        params = []

        # Apply filters only if not "All" or empty
        if status and status.lower() != "all":
            filters.append("UPPER(o.status) = UPPER(?)")
            params.append(status)

        # Date filters
        if start_date:
            valid_start_date = validate_date(start_date)
            if valid_start_date: # Ensure validation didn't return None
                filters.append("DATE(o.created_date) >= DATE(?)")
                params.append(valid_start_date)

        if end_date:
            valid_end_date = validate_date(end_date)
            if valid_end_date: # Ensure validation didn't return None
                filters.append("DATE(o.created_date) <= DATE(?)")
                params.append(valid_end_date)

        # Requester filter (using LIKE for partial match as per your analysis)
        if requester and requester.lower() != "all":
            filters.append("UPPER(r.name) LIKE UPPER(?)")
            params.append(f"%{requester}%")

        # Supplier filter (using LIKE for partial match as per your analysis)
        if supplier and supplier.lower() != "all":
            filters.append("UPPER(s.name) LIKE UPPER(?)")
            params.append(f"%{supplier}%")

        # Order Number filter (using LIKE for partial match as per your analysis)
        if order_number:
            filters.append("o.order_number LIKE ?")
            params.append(f"%{order_number}%")
            
        # You might want to explicitly exclude 'Deleted' orders from the main view
        # if that's desired for the default audit trail view, similar to other screens.
        # Example: filters.append("UPPER(o.status) != 'DELETED'")

        where_clause = " AND ".join(filters) if filters else "1=1"

        # REWRITTEN SQL query for robust filtering and latest audit user retrieval
        cursor = conn.execute(f"""
            SELECT
                o.id, o.created_date, o.received_date, o.order_number,
                r.name AS requester, s.name AS supplier,
                o.order_note, o.note_to_supplier, o.total, o.status,
                latest_audit_user.username AS audit_user, -- User for the latest action
                created_user.username AS created_by_user, -- User who created the order
                authorised_user.username AS authorised_by_user, -- User who authorised the order
                paid_user.username AS paid_by_user, -- User who marked COD paid
                received_user.username AS received_by_user -- User who received the order
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            
            -- Join for the user who created the order (first 'Created' entry)
            LEFT JOIN (
                SELECT order_id, user_id
                FROM audit_trail
                WHERE action = 'Created'
                ORDER BY action_date ASC LIMIT 1
            ) ac ON ac.order_id = o.id
            LEFT JOIN users created_user ON ac.user_id = created_user.id

            -- Join for the user who authorised the order (latest 'Authorised' entry)
            LEFT JOIN (
                SELECT order_id, user_id
                FROM audit_trail
                WHERE action = 'Authorised'
                ORDER BY action_date DESC LIMIT 1
            ) aa ON aa.order_id = o.id
            LEFT JOIN users authorised_user ON aa.user_id = authorised_user.id

            -- Join for the user who marked COD Paid (latest 'Marked COD Paid' entry)
            LEFT JOIN (
                SELECT order_id, user_id
                FROM audit_trail
                WHERE action = 'Marked COD Paid'
                ORDER BY action_date DESC LIMIT 1
            ) ap ON ap.order_id = o.id
            LEFT JOIN users paid_user ON ap.user_id = paid_user.id

            -- Join for the user who received the order (latest 'Received' entry)
            LEFT JOIN (
                SELECT order_id, user_id
                FROM audit_trail
                WHERE action = 'Received'
                ORDER BY action_date DESC LIMIT 1
            ) ar ON ar.order_id = o.id
            LEFT JOIN users received_user ON ar.user_id = received_user.id

            -- Join for the user of the *absolute latest* audit_trail entry (for main display 'User' column)
            LEFT JOIN ( 
                SELECT at_inner.order_id, at_inner.user_id, MAX(at_inner.action_date) AS latest_action_date
                FROM audit_trail at_inner
                GROUP BY at_inner.order_id
            ) AS latest_audit_record ON latest_audit_record.order_id = o.id
            LEFT JOIN users latest_audit_user ON latest_audit_record.user_id = latest_audit_user.id

            WHERE {where_clause}
            ORDER BY o.created_date DESC, o.order_number DESC
        """, params) 

        orders = [dict(row) for row in cursor.fetchall()]

        for order in orders:
            # Reformat created_date
            if order["created_date"]:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                order["created_date"] = "N/A"

            # Reformat received_date
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
            "filters": {"status": status, "start_date": start_date, "end_date": end_date, "requester": requester, "supplier": supplier, "order_number": order_number}
        })
        return {"orders": orders}

    except Exception as e:
        log_event("audit_trail_log.txt", {"error": str(e), "type": "audit_trail_orders_filtered"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail orders: {e}")
    finally:
        conn.close()