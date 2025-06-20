import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

from backend.utils.db_utils import handle_db_errors, log_success, log_warning
from backend.utils.order_utils import calculate_order_total
from backend.database import create_order, get_db_connection

router = APIRouter(tags=["orders"])

# --- Models ---
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
    payment_terms: Optional[str] = None  # ✅ Add this
    items: List[OrderItemCreate]
    auth_band_required: Optional[int] = None

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

        # --- Allow relaxed validation for drafts ---
        if order.status != "Draft":
            for item in order.items:
                if not item.item_code or not item.project or item.qty_ordered <= 0 or item.price <= 0:
                    raise HTTPException(status_code=400, detail="Invalid item: all fields required for non-draft orders")
            total = calculate_order_total([item.dict() for item in order.items])
        else:
            total = 0.0  # Safe default for Drafts

        order_data = {
            "order_number": order.order_number,
            "status": order.status,
            "total": total,
            "order_note": order.order_note,
            "note_to_supplier": order.note_to_supplier,
            "supplier_id": order.supplier_id,
            "requester_id": order.requester_id,
            "payment_terms": order.payment_terms,
            "auth_band_required": order.auth_band_required
        }

        items = [item.dict() for item in order.items]
        result = create_order(order_data, items)
        log_success("order", "created", f"Order {order.order_number} with status {order.status} and total R{total}")
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

@router.put("/update_draft/{order_id}")
@handle_db_errors(entity="draft_order", action="updating")
async def update_draft_order(order_id: int, payload: dict):
    items = payload.get("items", [])
    if not items:
        raise HTTPException(status_code=400, detail="No items provided")

    conn = get_db_connection()
    cursor = conn.cursor()

    for item in items:
        item_id = item.get("item_id")
        try:
            qty = float(item.get("quantity", 0))
            price = float(item.get("unit_price", 0))
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid quantity or price format")

        if item_id is None:
            raise HTTPException(status_code=400, detail="Missing item_id")

        total = qty * price

        cursor.execute("""
            UPDATE order_items
            SET qty_ordered = ?, price = ?, total = ?
            WHERE id = ? AND order_id = ?
        """, (qty, price, total, item_id, order_id))

    # ✅ Recalculate and update order total and status
    cursor.execute("""
        UPDATE orders
        SET total = (SELECT SUM(qty_ordered * price) FROM order_items WHERE order_id = ?),
            status = 'Pending'
        WHERE id = ? AND status = 'Draft'
    """, (order_id, order_id))

    # ✅ Optional: Return new total
    cursor.execute("SELECT total FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    new_total = row["total"] if row else 0.0

    conn.commit()
    conn.close()
    log_success("draft_order", "updated", f"Draft order {order_id} submitted as Pending")

    return {"message": "Draft order updated and submitted", "new_total": new_total}

@router.get("/api/order_items/{order_id}")
@handle_db_errors(entity="order_items", action="fetching")
async def get_items_for_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, item_code, item_description, project,
                qty_ordered AS quantity,
                price AS unit_price
        FROM order_items
        WHERE order_id = ?

    """, (order_id,))
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("order_items", "fetched", f"{len(result)} items for order {order_id}")
    return result  # frontend expects raw array

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

@router.get("/api/audit_trail_orders")
@handle_db_errors(entity="orders", action="fetching all")
async def get_audit_trail_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
            o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
            s.name AS supplier,
            r.name AS requester,
            u.username AS audit_user
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
        LEFT JOIN (
            SELECT order_id, MAX(action_date) AS latest_action_date
            FROM audit_trail
            WHERE action = 'Authorised'
            GROUP BY order_id
        ) latest_auth ON latest_auth.order_id = o.id
        LEFT JOIN audit_trail at ON at.order_id = o.id AND at.action_date = latest_auth.latest_action_date
        LEFT JOIN users u ON at.user_id = u.id
        ORDER BY o.created_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("audit_trail_orders", "fetched", f"{len(result)} total orders for audit trail")
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
