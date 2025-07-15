# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/order_queries.py

from pydantic import BaseModel
from backend.database import get_db_connection
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List, Dict
from datetime import datetime
import sqlite3
from pathlib import Path
import json

from backend.utils.permissions_utils import require_login

router = APIRouter(tags=["orders"])

def log_event(filename: str, data: dict):
    """Logs an event to a file."""
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

class CodPaymentPayload(BaseModel):
    amount_paid: float
    payment_date: str  # Expected format:YYYY-MM-DD

def validate_date(date_str: Optional[str]) -> Optional[str]:
    """Helper function to validate date strings."""
    if not date_str:
        return None
    try:
        # Try to parse various formats to ensure flexibility, then return YYYY-MM-DD
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


@router.get("/pending_orders")
async def get_pending_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user: Dict = Depends(require_login)
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters = []
        params = []

        # Default filters for pending orders screen
        filters.append("UPPER(o.status) IN ('PENDING', 'WAITING FOR APPROVAL', 'AWAITING AUTHORISATION', 'AUTHORISED', 'DRAFT', 'PAID', 'PARTIALLY RECEIVED')")
        filters.append("UPPER(o.status) != 'DELETED'")


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

        if status is not None and status.strip().lower() != "all" and status.strip() != "":
            filters.append("UPPER(o.status) = UPPER(?)")
            params.append(status.strip())

        where_clause = " AND ".join(filters) if filters else "1=1"

        cursor = conn.execute(f"""
            SELECT
                o.id, o.created_date, o.order_number,
                r.name AS requester, s.name AS supplier,
                o.order_note, o.note_to_supplier, o.total, o.status
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            WHERE {where_clause}
            ORDER BY
                CAST(SUBSTR(o.order_number, INSTR(o.order_number, 'C') + 1) AS INTEGER) DESC,
                o.created_date DESC
        """, params)
        orders = [dict(row) for row in cursor.fetchall()]
        for order in orders:
            if order["created_date"]:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
                    except ValueError:
                        order["created_date"] = "N/A"
            else:
                order["created_date"] = "N/A"
        log_event("new_orders_log.txt", {"action": "fetch_pending_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "pending_orders"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "pending_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load pending orders: {e}")
    finally:
        conn.close()


@router.get("/received_orders")
async def get_received_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user: Dict = Depends(require_login)
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters = []
        params = []

        # Allow status filter to override or combine
        if status is not None and status.strip().lower() != "all" and status.strip() != "":
            filters.append("UPPER(o.status) = UPPER(?)")
            params.append(status.strip())
        else:
            # Default to showing both 'Received' and 'Partially Received' if 'All' or no status is specified
            filters.append("UPPER(o.status) IN ('RECEIVED', 'PARTIALLY RECEIVED')")

        filters.append("UPPER(o.status) != 'DELETED'")

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

        cursor = conn.execute(f"""
            SELECT
                o.id, o.created_date, o.order_number,
                r.name AS requester, s.name AS supplier,
                o.order_note, o.note_to_supplier, o.total, o.status
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            WHERE {where_clause}
            ORDER BY
                CAST(SUBSTR(o.order_number, INSTR(o.order_number, 'C') + 1) AS INTEGER) DESC,
                o.created_date DESC
        """, params)
        orders = [dict(row) for row in cursor.fetchall()]
        for order in orders:
            if order["created_date"]:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
                    except ValueError:
                        order["created_date"] = "N/A"
            else:
                order["created_date"] = "N/A"
        log_event("new_orders_log.txt", {"action": "fetch_received_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load received orders: {e}")
    finally:
        conn.close()

@router.get("/partially_delivered")
async def get_partially_delivered_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    user: Dict = Depends(require_login)
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters = ["oi.qty_received < oi.qty_ordered", "UPPER(o.status) != 'CANCELLED'", "UPPER(o.status) != 'DELETED'"]
        params = []

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

        cursor = conn.execute(f"""
            SELECT DISTINCT o.id, o.created_date, o.order_number,
                r.name AS requester, s.name AS supplier,
                o.order_note, o.note_to_supplier, o.total, o.status
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            JOIN order_items oi ON o.id = oi.order_id
            WHERE {where_clause}
            ORDER BY
                CAST(SUBSTR(o.order_number, INSTR(o.order_number, 'C') + 1) AS INTEGER) DESC,
                o.created_date DESC
        """, params)
        orders = [dict(row) for row in cursor.fetchall()]
        for order in orders:
            if order["created_date"]:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
                    except ValueError:
                        order["created_date"] = "N/A"
            else:
                order["created_date"] = "N/A"
        return {"orders": orders}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "partially_delivered"})
        raise HTTPException(status_code=500, detail=f"Failed to fetch partially delivered orders: {e}")
    finally:
        conn.close()

@router.get("/items_for_order/{order_id}")
async def get_items_for_order(order_id: int, user: Dict = Depends(require_login)):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute("""
            SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date, price,
                   (qty_ordered * price) AS total
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        items = [dict(row) for row in cursor.fetchall()]
        log_event("new_orders_log.txt", {"action": "fetch_items_for_order", "order_id": order_id, "count": len(items)})
        return {"items": items}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "items_for_order"})
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {e}")
    finally:
        conn.close()

# The following function is being REMOVED to resolve endpoint conflict
# @router.get("/orders/api/audit_trail_orders")
# async def get_audit_trail_orders(
#     status: Optional[str] = Query(None, description="Filter by order status"),
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
#     requester: Optional[str] = Query(None),
#     supplier: Optional[str] = Query(None),
#     user: Dict = Depends(require_login)
# ):
#     conn = get_db_connection()
#     conn.row_factory = sqlite3.Row
#     try:
#         filters = []
#         params = []

#         # Standardized status filtering
#         if status is not None and status.strip().lower() != "all" and status.strip() != "":
#             filters.append("UPPER(o.status) = UPPER(?)")
#             params.append(status.strip())

#         # Standardized date filters
#         if start_date:
#             valid_start_date = validate_date(start_date)
#             filters.append("DATE(o.created_date) >= DATE(?)")
#             params.append(valid_start_date)

#         if end_date:
#             valid_end_date = validate_date(end_date)
#             filters.append("DATE(o.created_date) <= DATE(?)")
#             params.append(valid_end_date)

#         # Filter by requester, ensuring "All" is skipped
#         if requester is not None and requester.strip().lower() != "all" and requester.strip() != "":
#             filters.append("UPPER(r.name) LIKE UPPER(?)")
#             params.append(f"%{requester.strip()}%")

#         # Filter by supplier, ensuring "All" is skipped
#         if supplier is not None and supplier.strip().lower() != "all" and supplier.strip() != "":
#             filters.append("UPPER(s.name) LIKE UPPER(?)")
#             params.append(f"%{supplier.strip()}%")

#         where_clause = " AND ".join(filters) if filters else "1=1"

#         # --- DEBUGGING LOG ENTRY ---
#         log_event("audit_trail_debug_log.txt", {
#             "debug_point": "pre_execute_audit_query",
#             "filters_list": filters,
#             "params_list": params,
#             "final_where_clause": where_clause
#         })
#         print(f"\n--- DEBUG AUDIT TRAIL QUERY CONSTRUCTION ---")
#         print(f"Filters List: {filters}")
#         print(f"Parameters List: {params}")
#         print(f"Final WHERE Clause: {where_clause}")
#         print(f"--------------------------------------------\n")
#         # --- END DEBUGGING LOG ENTRY ---

#         cursor = conn.execute(f"""
#             SELECT
#                 o.id, o.created_date, o.received_date, o.order_number,
#                 r.name AS requester, s.name AS supplier,
#                 o.order_note, o.note_to_supplier, o.total, o.status,
#                 u_auth.username AS audit_user,
#                 ap.action_date AS paid_date,
#                 ap.details AS paid_details,
#                 u_paid.username AS paid_by_user
#             FROM orders o
#             LEFT JOIN requesters r ON o.requester_id = r.id
#             LEFT JOIN suppliers s ON o.supplier_id = s.id
#             LEFT JOIN (
#                 SELECT order_id, MAX(action_date) AS latest_action_date, user_id
#                 FROM audit_trail
#                 WHERE action = 'Authorised'
#                 GROUP BY order_id
#             ) latest_auth ON latest_auth.order_id = o.id
#             LEFT JOIN users u_auth ON latest_auth.user_id = u_auth.id
#             LEFT JOIN (
#                 SELECT order_id, MAX(action_date) AS action_date, details, user_id
#                 FROM audit_trail
#                 WHERE action = 'Marked COD Paid'
#                 GROUP BY order_id
#             ) ap ON ap.order_id = o.id
#             LEFT JOIN users u_paid ON ap.user_id = u_paid.id
#             WHERE {where_clause}
#             GROUP BY o.id
#             ORDER BY
#                 CAST(SUBSTR(o.order_number, INSTR(o.order_number, 'C') + 1) AS INTEGER) DESC,
#                 o.created_date DESC
#         """, params)

#         orders = [dict(row) for row in cursor.fetchall()]

#         # Format dates for display
#         for order in orders:
#             # Handle created_date
#             if order["created_date"]:
#                 try:
#                     order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
#                 except ValueError:
#                     try:
#                         order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
#                     except ValueError:
#                          order["created_date"] = "N/A"
#             else:
#                 order["created_date"] = "N/A"

#             # Handle received_date
#             if order["received_date"]:
#                 try:
#                     order["received_date"] = datetime.strptime(order["received_date"], "%Y-%m-%d %H:%M:%M").strftime("%Y-%m-%d")
#                 except ValueError:
#                     try:
#                         order["received_date"] = datetime.strptime(order["received_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
#                     except ValueError:
#                         order["received_date"] = "N/A"
#             else:
#                 order["received_date"] = "N/A"

#             # NEW: Format paid_date if exists
#             if order["paid_date"]:
#                 try:
#                     order["paid_date"] = datetime.strptime(order["paid_date"], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M")
#                 except ValueError:
#                     # Fallback for other potential formats if necessary
#                     order["paid_date"] = "N/A"


#         # Log the activity (standard log, not debug log)
#         log_event("audit_trail_log.txt", {
#             "action": "fetch_audit_trail_orders",
#             "count": len(orders),
#             "filters": {
#                 "status": status,
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "requester": requester,
#                 "supplier": supplier
#             }
#         })
#         return {"orders": orders}

#     except Exception as e:
#         print(f"Error in get_audit_trail_orders: {e}")
#         # Log error with received filters for better debugging
#         log_event("audit_trail_log.txt", {
#             "error": str(e),
#             "type": "audit_trail_orders",
#             "filters_received_on_error": {
#                 "status": status,
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "requester": requester,
#                 "supplier": supplier
#             }
#         })
#         raise HTTPException(status_code=500, detail=f"Failed to load audit trail orders: {e}")
#     finally:
#         conn.close()

@router.get("/last_audit_action/{order_id}")
async def get_last_audit_action(order_id: int, user: Dict = Depends(require_login)):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT details, action_date
            FROM audit_trail
            WHERE order_id = ?
            ORDER BY action_date DESC
            LIMIT 1
        """, (order_id,))
        row = cursor.fetchone()
        if row:
            return {"details": row["details"], "action_date": row["action_date"]}
        else:
            return {"details": "No actions yet", "action_date": None}
    except Exception as e:
        print(f"Error in get_last_audit_action: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch last audit action: {e}")
    finally:
        conn.close()


@router.get("/order_summary")
async def get_order_summary(user: Dict = Depends(require_login)):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN UPPER(status) = 'PENDING' THEN 1 ELSE 0 END), 0) AS pending,
                COALESCE(SUM(CASE WHEN UPPER(status) = 'AWAITING AUTHORISATION' THEN 1 ELSE 0 END), 0) AS awaiting,
                COALESCE(SUM(CASE WHEN UPPER(status) = 'AUTHORISED' THEN 1 ELSE 0 END), 0) AS authorised,
                COALESCE(SUM(CASE WHEN UPPER(status) = 'RECEIVED' THEN 1 ELSE 0 END), 0) AS received,
                COUNT(*) AS total
            FROM orders
        """)
        row = cursor.fetchone()
        return {
            "pending": row[0],
            "awaiting": row[1],
            "authorised": row[2],
            "received": row[3],
            "total": row[4]
        }
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "order_summary"})
        raise HTTPException(status_code=500, detail=f"Failed to load order summary: {e}")
    finally:
        conn.close()

@router.get("/cod_orders")
async def get_cod_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user: Dict = Depends(require_login)
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters = [] # Start with an empty list
        params = []

        filters.append("UPPER(o.payment_terms) = 'COD'") # Always filter for COD

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

        if status is not None and status.strip().lower() != "all" and status.strip() != "":
            filters.append("UPPER(o.status) = UPPER(?)")
            params.append(status.strip())

        where_clause = " AND ".join(filters) if filters else "1=1"

        cursor = conn.execute(f"""
            SELECT
                o.id, o.created_date, o.order_number,
                r.name AS requester, s.name AS supplier,
                o.order_note, o.note_to_supplier, o.total, o.status
            FROM orders o
            LEFT JOIN requesters r ON o.requester_id = r.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            WHERE {where_clause}
            AND UPPER(o.status) != 'DELETED' -- This Python comment is now correctly outside the f-string
            ORDER BY
                CAST(SUBSTR(o.order_number, INSTR(o.order_number, 'C') + 1) AS INTEGER) DESC,
                o.created_date DESC
        """, params)
        orders = [dict(row) for row in cursor.fetchall()]
        for order in orders:
            if order["created_date"]:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
                    except ValueError:
                        order["created_date"] = "N/A"
            else:
                order["created_date"] = "N/A"
        log_event("new_orders_log.txt", {"action": "fetch_cod_orders", "count": len(orders)})
        return {"orders": orders}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "cod_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to fetch COD orders: {e}")
    finally:
        conn.close()

@router.put("/mark_cod_paid/{order_id}")
async def mark_cod_paid(order_id: int, payload: CodPaymentPayload, user: Dict = Depends(require_login)):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders
            SET amount_paid = ?, payment_date = ?
            WHERE id = ?
        """, (payload.amount_paid, payload.payment_date, order_id))
        conn.commit()

        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, action_date, details, user_id)
            VALUES (?, ?, datetime('now'), ?, ?)
        """, (
            order_id,
            "Marked COD Paid",
            f"Amount: R{payload.amount_paid:.2f}, Date: {payload.payment_date}",
            user['id']
        ))
        conn.commit()

        return {"success": True}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "mark_cod_paid"})
        raise HTTPException(status_code=500, detail=f"Failed to mark COD paid: {e}")
    finally:
        conn.close()