from fastapi import APIRouter, HTTPException, Request
from backend.database import get_db_connection
import logging
import json
from datetime import datetime
from typing import Dict, Any
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/new_orders_log.txt", level=logging.INFO, format="[%(asctime)s] %(message)s")

# Helper function to get current timestamp
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

@router.post("/")
async def create_order(request: Dict[str, Any]):
    order_data = request
    order_number = order_data.get("order_number")
    requester_id = order_data.get("requester_id")
    supplier_id = order_data.get("supplier_id")
    note_to_supplier = order_data.get("note_to_supplier", "")
    items = order_data.get("items", [])

    if not all([order_number, requester_id, supplier_id, items]):
        logging.error("Missing required fields in order creation request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validate requester_id
        cursor.execute("SELECT id FROM requesters WHERE id = ?", (requester_id,))
        if not cursor.fetchone():
            logging.error(f"Invalid requester_id: {requester_id}")
            raise HTTPException(status_code=400, detail=f"Requester with ID {requester_id} does not exist")

        # Validate supplier_id
        cursor.execute("SELECT id FROM suppliers WHERE id = ?", (supplier_id,))
        if not cursor.fetchone():
            logging.error(f"Invalid supplier_id: {supplier_id}")
            raise HTTPException(status_code=400, detail=f"Supplier with ID {supplier_id} does not exist")

        total = sum(item["qty_ordered"] * item["price"] for item in items)
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert the order
        cursor.execute("""
            INSERT INTO orders (order_number, status, created_date, total, order_note, note_to_supplier, supplier_id, requester_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_number, "Pending", created_date, total, "", note_to_supplier, supplier_id, requester_id))
        order_id = cursor.lastrowid

        # Insert order items
        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, item_code, item_description, project, qty_ordered, price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, item["item_code"], item["item_description"], item["project"], item["qty_ordered"], item["price"]))

        conn.commit()
        logging.info(json.dumps({"action": "submit_success", "order_number": order_number, "status": "Pending", "order_id": order_id}))
        return {"message": "Order created successfully", "order": {"id": order_id}}
    except sqlite3.Error as e:
        logging.error(f"Database error during order creation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

@router.get("/api/orders/pending_orders")
async def get_pending_orders(start_date: str = None, end_date: str = None, requester: str = None, supplier: str = None, status: str = None):
    query = """
        SELECT o.id, o.order_number, o.created_date, o.total, o.status, o.note_to_supplier, o.order_note,
               r.name as requester, s.name as supplier
        FROM orders o
        LEFT JOIN requesters r ON o.requester_id = r.id
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        WHERE o.status IN ('Pending', 'Waiting for Approval', 'Awaiting Authorisation', 'Authorised')
    """
    params = []

    try:
        if start_date:
            datetime.strptime(start_date, "%Y-%m-%d")
            query += " AND o.created_date >= ?"
            params.append(start_date)
        if end_date:
            datetime.strptime(end_date, "%Y-%m-%d")
            query += " AND o.created_date <= ?"
            params.append(end_date)
    except ValueError as e:
        logging.error(f"Invalid date format: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if requester and requester != "All":
        query += " AND r.name = ?"
        params.append(requester)
    if supplier and supplier != "All":
        query += " AND s.name = ?"
        params.append(supplier)
    if status and status != "All":
        query += " AND o.status = ?"
        params.append(status)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        orders = cursor.fetchall()

        result = []
        for order in orders:
            result.append({
                "id": order[0],
                "order_number": order[1],
                "created_date": order[2],
                "total": float(order[3]) if order[3] is not None else 0.0,
                "status": order[4],
                "note_to_supplier": order[5] or "",
                "order_note": order[6] or "",
                "requester": order[7] or "Unknown",
                "supplier": order[8] or "Unknown"
            })

        logging.info(json.dumps({"action": "fetch_pending_orders", "count": len(result), "params": params}))
        return {"orders": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching pending orders: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching pending orders: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching pending orders: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

@router.get("/api/audit_trail")
async def get_audit_trail():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_trail'")
        table_exists = cursor.fetchone()
        if not table_exists:
            logging.error("Audit trail table does not exist in the database")
            raise HTTPException(status_code=500, detail="Audit trail table does not exist")

        cursor.execute("SELECT id, order_id, action, action_date FROM audit_trail ORDER BY action_date DESC")
        audit_entries = cursor.fetchall()

        result = []
        for entry in audit_entries:
            result.append({
                "id": entry[0],
                "order_id": entry[1],
                "action": entry[2],
                "timestamp": entry[3]
            })

        logging.info(json.dumps({"action": "fetch_audit_trail", "count": len(result)}))
        return {"audit_trail": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching audit trail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching audit trail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching audit trail: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
