# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

# --- IMPORTANT FIX: Added log_error to the import ---
from backend.utils.db_utils import handle_db_errors, log_success, log_warning, log_error
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
    payment_terms: Optional[str] = None
    created_date: Optional[str] = None
    items: List[OrderItemCreate]
    auth_band_required: Optional[int] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    requester_id: Optional[int] = None

# --- FIX START: Retaining only the first definition of these models ---
# These models were duplicated further down, which caused the NameError.
# They are now correctly defined ONLY ONCE here at the top.
class ReceivedItem(BaseModel):
    item_id: int
    received_qty: float

class ReceivePayload(BaseModel):
    items: List[ReceivedItem]
# --- FIX END ---

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
        
        result = create_order(order_data, items, created_date=order.created_date)
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

@handle_db_errors(entity="order", action="deleting")
@router.delete("/delete/{order_id}")
async def delete_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'Deleted' WHERE id = ?", (order_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found or already deleted")
    conn.commit()
    conn.close()
    log_success("order", "deleted", f"Order {order_id} marked as Deleted")
    return {"message": "Order deleted and moved to audit trail"}

@router.get("/{order_id}")
@handle_db_errors(entity="order", action="fetching")
async def get_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
               o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
               s.name as supplier_name, r.name as requester_name,
               o.payment_date, o.amount_paid
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

# NEW ENDPOINT: To fetch specific order details for expanded view on audit trail
@router.get("/api/order_details_for_audit/{order_id}")
@handle_db_errors(entity="order_details", action="fetching for audit")
async def get_order_details_for_audit(order_id: int):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                o.id,
                o.status,
                o.amount_paid,
                o.payment_date,
                o.order_note,
                o.note_to_supplier,
                o.total,               -- This maps to "Original Amount"
                s.name AS supplier_name, -- This maps to "Supplier"
                u_paid.username AS paid_by_user -- This maps to "User (who paid)"
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN (
                SELECT order_id, user_id, action_date
                FROM audit_trail
                WHERE action = 'Marked COD Paid'
                ORDER BY action_date DESC LIMIT 1
            ) ap ON ap.order_id = o.id
            LEFT JOIN users u_paid ON ap.user_id = u_paid.id
            WHERE o.id = ?
        """, (order_id,))
        order_details = cursor.fetchone()
        conn.close()
        if not order_details:
            raise HTTPException(status_code=404, detail="Order not found for audit details.")
        return dict(order_details)
    except Exception as e:
        log_error("order_details", "fetching for audit", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch order details for audit: {str(e)}")

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

    # Recalculate and update order total and status
    cursor.execute("""
        UPDATE orders
        SET total = (SELECT SUM(qty_ordered * price) FROM order_items WHERE order_id = ?),
            status = 'Pending'
        WHERE id = ? AND status = 'Draft'
    """, (order_id, order_id))

    # Optional: Return new total
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
        """, (item.received_qty, datetime.now().strftime("%Y-%m-%d"), item.item_id, order_id))

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
    conn.row_factory = sqlite3.Row # Ensure row_factory is set for this connection
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
            o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
            s.name AS supplier,
            r.name AS requester,
            auditor.username AS audit_user
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
        LEFT JOIN (
            SELECT
                at_inner.order_id,
                at_inner.user_id,
                MAX(at_inner.action_date) AS latest_action_date
            FROM audit_trail at_inner
            WHERE at_inner.action = 'Authorised'
            GROUP BY at_inner.order_id
        ) latest_auth_record ON latest_auth_record.order_id = o.id
        LEFT JOIN users auditor ON latest_auth_record.user_id = auditor.id
        ORDER BY o.order_number DESC -- FIX: Changed sorting to order_number descending
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