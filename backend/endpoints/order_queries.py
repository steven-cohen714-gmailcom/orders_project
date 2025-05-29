from pydantic import BaseModel
from backend.database import get_db_connection
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import json

router = APIRouter(tags=["orders"])

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.get("/pending_orders")
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
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                except ValueError:
                    try:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y")
                    except ValueError:
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
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                except ValueError:
                    try:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y")
                    except ValueError:
                        order["created_date"] = datetime.strptime(order["created_date"], "%Y/%m/%d").strftime("%d/%m/%Y")
        log_event("new_orders_log.txt", {"action": "fetch_received_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load received orders: {e}")

@router.get("/partially_delivered")
def get_partially_delivered_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                JOIN order_items oi ON o.id = oi.order_id
                WHERE oi.qty_received < oi.qty_ordered
                AND o.status != 'Cancelled'
                ORDER BY o.created_date DESC
            """)
            orders = [dict(row) for row in cursor.fetchall()]
            return {"orders": orders}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "partially_delivered"})
        raise HTTPException(status_code=500, detail=f"Failed to fetch partially delivered orders: {e}")

@router.get("/items_for_order/{order_id}")
def get_items_for_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
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
                    o.order_note, o.note_to_supplier, o.total, o.status,
                    (
                        SELECT 
                            COALESCE(at.action, 'No actions yet') ||
                            CASE 
                                WHEN u.username IS NOT NULL THEN ' by ' || u.username 
                                ELSE '' 
                            END ||
                            CASE 
                                WHEN at.action_date IS NOT NULL THEN ' at ' || at.action_date 
                                ELSE '' 
                            END
                        FROM audit_trail at
                        LEFT JOIN users u ON at.user_id = u.id
                        WHERE at.order_id = o.id
                        ORDER BY at.action_date DESC
                        LIMIT 1
                    ) AS last_action
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)

            orders = [dict(row) for row in cursor.fetchall()]

            for order in orders:
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                except:
                    pass
                if order["received_date"]:
                    try:
                        order["received_date"] = datetime.strptime(order["received_date"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                    except:
                        pass

                cursor.execute("""
                    SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date
                    FROM order_items
                    WHERE order_id = ?
                """, (order["id"],))
                order["items"] = [dict(item) for item in cursor.fetchall()]

        log_event("new_orders_log.txt", {"action": "fetch_audit_trail", "count": len(orders)})
        return {"orders": orders}

    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail: {e}")
    
@router.get("/last_audit_action/{order_id}")
def get_last_audit_action(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT details, action_date
        FROM audit_trail
        WHERE order_id = ?
        ORDER BY action_date DESC
        LIMIT 1
    """, (order_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"details": row["details"], "action_date": row["action_date"]}
    else:
        return {"details": "No actions yet", "action_date": None}

@router.get("/order_summary")
def get_order_summary():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END), 0) AS pending,
                    COALESCE(SUM(CASE WHEN status = 'Awaiting Authorisation' THEN 1 ELSE 0 END), 0) AS awaiting,
                    COALESCE(SUM(CASE WHEN status = 'Authorised' THEN 1 ELSE 0 END), 0) AS authorised,
                    COALESCE(SUM(CASE WHEN status = 'Received' THEN 1 ELSE 0 END), 0) AS received,
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

@router.get("/cod_orders")
def get_cod_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = ["o.payment_terms = 'COD'"]
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

        where_clause = " AND ".join(filters)

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
                try:
                    order["created_date"] = datetime.strptime(order["created_date"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                except:
                    pass
        log_event("new_orders_log.txt", {"action": "fetch_cod_orders", "count": len(orders)})
        return {"orders": orders}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "cod_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to fetch COD orders: {e}")
    
    from pydantic import BaseModel

class CodPaymentPayload(BaseModel):
    amount_paid: float
    payment_date: str  # Expected format: YYYY-MM-DD

@router.put("/mark_cod_paid/{order_id}")
def mark_cod_paid(order_id: int, payload: CodPaymentPayload):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders
                SET amount_paid = ?, payment_date = ?
                WHERE id = ?
            """, (payload.amount_paid, payload.payment_date, order_id))
            conn.commit()

            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, action_date, details)
                VALUES (?, ?, datetime('now'), ?)
            """, (
                order_id,
                "Marked COD Paid",
                f"Amount: R{payload.amount_paid:.2f}, Date: {payload.payment_date}"
            ))
            conn.commit()

        return {"success": True}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "mark_cod_paid"})
        raise HTTPException(status_code=500, detail=f"Failed to mark COD paid: {e}")

