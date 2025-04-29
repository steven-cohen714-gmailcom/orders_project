from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import json  # Add this import

router = APIRouter(prefix="/orders/api", tags=["orders"])

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.get("/orders/pending_orders")
def get_pending_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = []
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        # Include orders that are Pending, Waiting for Approval, Awaiting Authorisation, or Authorised
        filters.append("o.status IN ('Pending', 'Waiting for Approval', 'Awaiting Authorisation', 'Authorised')")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        if status and status != "All":
            filters.append("o.status = ?")
            params.append(status)

        where_clause = " AND ".join(filters) if filters else "1=1"

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = [dict(row) for row in cursor.fetchall()]
            for order in orders:
                # Try parsing the date in both possible formats
                try:
                    # First try the SQLite CURRENT_TIMESTAMP format (YYYY-MM-DDTHH:MM:SS.ssssss)
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y")
                except ValueError:
                    # If that fails, try the YYYY/MM/DD format from manual inserts
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y/%m/%d").strftime("%d/%m/%Y")
        log_event("new_orders_log.txt", {"action": "fetch_pending_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "pending_orders"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "pending_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load pending orders: {e}")

@router.get("/received_orders")
def get_received_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None)
):
    try:
        filters = ["o.status = 'Received'"]
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        where_clause = " AND ".join(filters) if filters else "1=1"

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = [dict(row) for row in cursor.fetchall()]
            for order in orders:
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
        log_event("new_orders_log.txt", {"action": "fetch_received_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load received orders: {e}")

@router.get("/items_for_order/{order_id}")
def get_items_for_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
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

@router.get("/audit_trail")
def get_audit_trail(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = []
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        if status and status != "All":
            filters.append("o.status = ?")
            params.append(status)

        where_clause = " AND ".join(filters) if filters else "1=1"

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.received_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = [dict(row) for row in cursor.fetchall()]
            for order in orders:
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                if order["received_date"]:
                    order["received_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                # Fetch items for this order
                cursor.execute("""
                    SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date
                    FROM order_items
                    WHERE order_id = ?
                """, (order["id"],))
                items = [dict(item_row) for item_row in cursor.fetchall()]
                for item in items:
                    if item["received_date"]:
                        item["received_date"] = datetime.fromisoformat(item["received_date"]).strftime("%d/%m/%Y")
                order["items"] = items
        log_event("new_orders_log.txt", {"action": "fetch_audit_trail", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail: {e}")