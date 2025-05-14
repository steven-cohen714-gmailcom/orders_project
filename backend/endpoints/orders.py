import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

from backend.utils.db_utils import handle_db_errors, log_success, log_warning
from backend.utils.order_utils import calculate_order_total
from backend.database import create_order, get_db_connection

router = APIRouter(tags=["orders"])  # Removed prefix="/orders"

# Pydantic models
class OrderItemCreate(BaseModel):
    item_code: str
    item_description: str
    project: Optional[str] = None
    qty_ordered: float
    price: float

class OrderCreate(BaseModel):
    order_number: str
    status: str
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: int
    requester_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    requester_id: Optional[int] = None

class ReceiveItem(BaseModel):
    item_id: int
    qty_received: float

class ReceivePayload(BaseModel):
    items: List[ReceiveItem]

# --- Routes ---
@router.post("")
async def create_new_order(order: OrderCreate):
    try:
        logging.info(f"🔍 Incoming order: {order}")
        total = calculate_order_total([item.dict() for item in order.items])
        order_data = {
            "order_number": order.order_number,
            "status": order.status,
            "total": total,
            "order_note": order.order_note,
            "note_to_supplier": order.note_to_supplier,
            "supplier_id": order.supplier_id,
            "requester_id": order.requester_id
        }
        items = [item.dict() for item in order.items]
        result = create_order(order_data, items)
        log_success("order", "created", f"Order {order.order_number} with total R{total}")
        return {"message": "Order created successfully", "order_id": result["id"]}
    except Exception as e:
        logging.exception("❌ Order creation failed")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
@handle_db_errors(entity="orders", action="fetching")
async def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
               o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
               s.name as supplier_name, r.name as requester_name
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
    """)
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("orders", "fetched", f"{len(result)} items")
    return {"orders": result}

@router.get("/{order_id}")
@handle_db_errors(entity="order", action="fetching")
async def get_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
               o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
               s.name as supplier_name, r.name as requester_name
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
        WHERE o.id = ?
    """, (order_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        log_warning("order", f"No order found with id {order_id}")
        raise HTTPException(status_code=404, detail="Order not found")
    log_success("order", "fetched", f"Order {row['order_number']}")
    return dict(row)

@router.put("/{order_id}")
@handle_db_errors(entity="order", action="updating")
async def update_order(order_id: int, order: OrderUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = {}
    if order.status:
        updates["status"] = order.status
    if order.order_note is not None:
        updates["order_note"] = order.order_note
    if order.note_to_supplier is not None:
        updates["note_to_supplier"] = order.note_to_supplier
    if order.supplier_id:
        updates["supplier_id"] = order.supplier_id
    if order.requester_id:
        updates["requester_id"] = order.requester_id

    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = tuple(updates.values()) + (order_id,)
    cursor.execute(f"UPDATE orders SET {set_clause} WHERE id = ?", values)

    if cursor.rowcount == 0:
        conn.close()
        log_warning("order", f"No order found with id {order_id}")
        raise HTTPException(status_code=404, detail="Order not found")

    conn.commit()
    conn.close()
    log_success("order", "updated", f"Order {order_id} updated with fields {list(updates.keys())}")
    return {"message": "Order updated successfully"}

@router.get("/api/items_for_order/{order_id}")
@handle_db_errors(entity="order_items", action="fetching")
async def get_items_for_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, item_code, item_description, project, qty_ordered, qty_received,
               received_date, price, total
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("order_items", "fetched", f"{len(result)} items for order {order_id}")
    return {"items": result}

@router.post("/orders/receive/{order_id}")
@handle_db_errors(entity="receive", action="processing")
async def mark_items_as_received(order_id: int, payload: ReceivePayload):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for item in payload.items:
        cursor.execute("""
            UPDATE order_items
            SET qty_received = ?, received_date = ?
            WHERE id = ? AND order_id = ?
        """, (item.qty_received, datetime.now().strftime("%Y-%m-%d"), item.item_id, order_id))

    cursor.execute("""
        UPDATE orders
        SET status = 'Received', received_date = ?
        WHERE id = ? AND status IN ('Pending', 'Awaiting Authorisation')
    """, (datetime.now().strftime("%Y-%m-%d"), order_id))

    conn.commit()
    conn.close()
    log_success("receive", "processed", f"Marked {len(payload.items)} items as received")
    return {"message": "Items marked as received"}

@router.get("/api/received_orders")
@handle_db_errors(entity="orders", action="fetching received")
async def get_received_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
               o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
               s.name as supplier, r.name as requester
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
        WHERE o.status IN ('Received', 'Partially Received')
        ORDER BY o.order_number ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("received_orders", "fetched", f"{len(result)} received/partial orders")
    return {"orders": result}

@router.get("/api/receipt_logs/{order_id}")
@handle_db_errors(entity="received_item_logs", action="fetching")
async def get_receipt_logs(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ril.order_item_id, ril.qty_received, ril.received_date, u.username
        FROM received_item_logs ril
        LEFT JOIN users u ON ril.received_by_user_id = u.id
        WHERE ril.order_item_id IN (
            SELECT id FROM order_items WHERE order_id = ?
        )
        ORDER BY ril.received_date ASC
    """, (order_id,))
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    log_success("receipt_logs", "fetched", f"{len(result)} logs for order {order_id}")
    return {"logs": result}

@router.get("/api/audit_trail_orders")
@handle_db_errors(entity="orders", action="fetching all")
async def get_audit_trail_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
               o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
               s.name as supplier, r.name as requester
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
        ORDER BY o.created_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("audit_trail_orders", "fetched", f"{len(result)} total orders for audit trail")
    return {"orders": result}
