# File: backend/endpoints/orders.py

import logging
from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from backend.utils.time_utils import now_utc_iso

from backend.utils.db_utils import handle_db_errors, log_success, log_warning, log_error
from backend.utils.order_utils import calculate_order_total
from backend.database import create_order, get_db_connection 
from .order_queries import validate_date
from backend.utils.email_and_alerts_engine import dispatch_reviewer_alert_for_creation

from backend.utils.statuses import (
    FOR_REVIEW,
    AUTHORISED,
    PENDING,
    PARTIALLY_PAID,
    FULLY_PAID,
    RECEIVED,
    PARTIALLY_RECEIVED,
    DELETED,
)

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
    auth_band_required: Optional[int] = None 
    items: List[OrderItemCreate]
    draft_id: Optional[int] = None # This field allows receiving the draft ID from the frontend.

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    requester_id: Optional[int] = None

class ReceivedItem(BaseModel):
    item_id: int
    received_qty: float

class ReceivePayload(BaseModel):
    items: List[ReceivedItem]

# --- NEW: Model for COD Payment ---
class CodPayment(BaseModel):
    amount_paid: float
    payment_date: str
    payment_status: str

# --- Routes ---
@router.post("")
async def create_new_order(order: OrderCreate, request: Request):
    try:
        logging.info(f"🔍 Incoming order: {order}")

        user = request.session.get("user")
        if not user or "id" not in user:
            raise HTTPException(status_code=401, detail="User not authenticated")
        current_user_id = user["id"]

        # Validate items for non-draft path
        for item in order.items:
            if not item.item_code or not item.project or item.qty_ordered <= 0 or item.price <= 0:
                raise HTTPException(status_code=400, detail="Invalid item: all fields required for non-draft orders")

        total = calculate_order_total([item.dict() for item in order.items])

        # FORCE: always For Review here; never set band
        order_data = {
            "order_number": order.order_number,
            "status": FOR_REVIEW,
            "total": total,
            "order_note": order.order_note,
            "note_to_supplier": order.note_to_supplier,
            "supplier_id": order.supplier_id,
            "requester_id": order.requester_id,
            "payment_terms": order.payment_terms,
            "required_auth_band": None
        }
        items = [item.dict() for item in order.items]

        result = await create_order(
            order_data, items, current_user_id,
            created_date=order.created_date, draft_id=order.draft_id
        )

        # DB write succeeded
        log_success("order", "created", f"Order {order.order_number} created in '{FOR_REVIEW}' with total R{total}")

        # Fire the Reviewer alert (creation/draft submit) — endpoint stays dumb
        try:
            dispatch_reviewer_alert_for_creation(result["id"])
        except Exception as e:
            logging.error(f"Non-fatal: reviewer alert dispatch failed for order_id={result['id']}: {e}")

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
async def delete_order(order_id: int, request: Request):
    # get current user from session
    user = request.session.get("user")
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    current_user_id = user["id"]

    # Permission gate: only users with 'can_delete_transactions' may delete
    can_delete = 1 if (user.get("can_delete_transactions") or 0) else 0
    if can_delete != 1:
        raise HTTPException(status_code=403, detail="Not authorized to delete transactions")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1) Mark as Deleted
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (DELETED, order_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found or already deleted")

        # 2) Write audit row: who + when

        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, "Deleted", "Order marked as Deleted", current_user_id, now_utc_iso()))

        conn.commit()
        log_success("order", "deleted", f"Order {order_id} marked as Deleted by user {current_user_id}")
        return {"success": True, "message": "Order deleted and moved to audit trail"}
    except Exception as e:
        conn.rollback()
        log_error("order", "deleting", str(e))
        raise
    finally:
        conn.close()

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

# MODIFIED ENDPOINT: To fetch specific order details for expanded view on audit trail
# Simplified to only fetch core order details, as specific users (created_by, paid_by)
# will now be looked up directly from the auditHistory array on the frontend.
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
                o.order_number,
                o.status,
                o.created_date,
                o.received_date,
                o.amount_paid,
                o.payment_date,
                o.order_note,
                o.note_to_supplier,
                o.total,
                s.name AS supplier_name,
                r.name AS requester_name
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN requesters r ON o.requester_id = r.id
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

# NEW ENDPOINT: To fetch full audit history for an order
@router.get("/api/order_audit_history/{order_id}")
@handle_db_errors(entity="order_audit_history", action="fetching")
async def get_order_audit_history(order_id: int):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                at.action_date,
                at.action,
                at.details,
                u.username
            FROM audit_trail at
            LEFT JOIN users u ON at.user_id = u.id
            WHERE at.order_id = ?
            ORDER BY at.action_date DESC
        """, (order_id,))
        audit_history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return audit_history
    except Exception as e:
        log_error("order_audit_history", "fetching", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch order audit history: {str(e)}")

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
    """
    Safe draft update:
    - Recalculates total from items.
    - Forces status = 'For Review'.
    - Clears required_auth_band (NULL).
    - NO emails here (authoriser/COD fire only after review).
    """
    logging.info(f"🔄 Submitting draft order ID: {order_id}")

    items = payload.get("items", []) or []

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1) Update order_items if provided
        for item in items:
            item_id = item.get("item_id")
            if item_id is None:
                raise HTTPException(status_code=400, detail="Missing item_id in draft update payload")

            try:
                qty = float(item.get("quantity", 0) or 0)
                price = float(item.get("unit_price", 0) or 0)
            except (TypeError, ValueError) as e:
                raise HTTPException(status_code=400, detail=f"Invalid quantity/price for item {item_id}: {e}")

            cursor.execute("""
                UPDATE order_items
                SET qty_ordered = ?, price = ?
                WHERE id = ? AND order_id = ?
            """, (qty, price, item_id, order_id))

        # 2) Recompute total
        cursor.execute("""
            SELECT COALESCE(SUM(oi.qty_ordered * oi.price), 0) AS calculated_total
            FROM order_items oi
            WHERE oi.order_id = ?
        """, (order_id,))
        row = cursor.fetchone()
        new_order_total = row["calculated_total"] if row else 0.0

        # 3) Force Review-first state; no band yet
        cursor.execute("""
            UPDATE orders
            SET total = ?, status = ?, required_auth_band = NULL
            WHERE id = ?
        """, (new_order_total, FOR_REVIEW, order_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Draft order not found")

        # 4) Audit trail
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
            VALUES (?, 'Submitted for Review', 'Draft updated and submitted for review', NULL, ?)
        """, (order_id, now_utc_iso()))

        conn.commit()
        log_success(
            "draft_order",
            "updated",
            f"Draft order {order_id} -> {FOR_REVIEW} (no band at submit). Total={new_order_total}"
        )

        # Reviewer alert when draft is submitted for review (same as a new order ready for review)
        try:
            dispatch_reviewer_alert_for_creation(order_id)
        except Exception as e:
            logging.error(f"Non-fatal: reviewer alert dispatch failed for submitted draft order_id={order_id}: {e}")

        return {"message": "Draft order submitted for review", "new_total": new_order_total}

    except Exception as e:
        conn.rollback()
        logging.exception(f"❌ Error updating draft order {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update draft")
    finally:
        conn.close()

@router.get("/api/order_items/{order_id}")
@handle_db_errors(entity="order_items", action="fetching")
async def get_items_for_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            oi.id, 
            oi.item_code, 
            oi.item_description, 
            oi.project AS project_code,
            p.project_name, 
            oi.qty_ordered AS quantity,
            oi.price AS unit_price
        FROM order_items oi
        LEFT JOIN projects p ON oi.project = p.project_code
        WHERE oi.order_id = ?
    """, (order_id,))
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("order_items", "fetched", f"{len(result)} items for order {order_id}")
    return result # frontend expects raw array

@router.post("/receive/{order_id}")
@handle_db_errors(entity="receive", action="processing")
async def mark_items_as_received(order_id: int, payload: ReceivePayload):
    """
    Allow receiving when order is Pending, Authorised, Partially Received, Partially Paid, or Fully Paid.
    Receiving should not be blocked by payment status.

    New status after update:
      - 'Received' if all items fully received
      - 'Partially Received' otherwise
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 0) Current status gate (relaxed)
    cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    current_status = (row["status"] or "").strip()

    allowed_statuses = {PENDING, AUTHORISED, PARTIALLY_RECEIVED, PARTIALLY_PAID, FULLY_PAID}
    if current_status not in allowed_statuses:
        raise HTTPException(
            status_code=403,
            detail=f"Failed to receive order: 403: Order must be 'Pending', 'Authorised', 'Partially Received', 'Partially Paid', or 'Fully Paid' before receiving. Current status: {current_status}"
        )

    # 1) Apply item receipts
    for item in payload.items:
        cursor.execute("""
            UPDATE order_items
            SET qty_received = COALESCE(?, 0),
                received_date = ?
            WHERE id = ? AND order_id = ?
        """, (item.received_qty, now_utc_iso(), item.item_id, order_id))

    # 2) Recompute whether fully received
    cursor.execute("""
        SELECT
            SUM(qty_ordered) AS total_ordered,
            SUM(COALESCE(qty_received,0)) AS total_received,
            SUM(CASE WHEN COALESCE(qty_received,0) >= COALESCE(qty_ordered,0) THEN 1 ELSE 0 END) AS lines_fully_received,
            COUNT(*) AS lines_total
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))
    sums = cursor.fetchone()
    lines_fully = int(sums["lines_fully_received"] or 0)
    lines_total = int(sums["lines_total"] or 0)
    fully_received = (lines_total > 0 and lines_fully == lines_total)

    # 3) Set order status
    new_status = RECEIVED if fully_received else PARTIALLY_RECEIVED
    cursor.execute("""
        UPDATE orders
        SET status = ?, received_date = ?
        WHERE id = ?
    """, (new_status, now_utc_iso(), order_id))

    # 4) Audit
    cursor.execute("""
        INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
        VALUES (?, 'Receipt', ?, NULL, ?)
    """, (order_id, f"Items marked received; order status → {RECEIVED if fully_received else PARTIALLY_RECEIVED}", now_utc_iso()))

    conn.commit()
    conn.close()
    return {"message": f"Items marked as received; order is now '{new_status}'"}

@router.get("/api/audit_trail_orders")
@handle_db_errors(entity="orders", action="fetching all")
async def get_audit_trail_orders(
    status: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    order_number: Optional[str] = Query(None),
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row # Ensure row_factory is set for this connection
    cursor = conn.cursor()
    filters = []
    params = []

    if status and status.lower() != "all":
        filters.append("UPPER(o.status) = UPPER(?)")
        params.append(status)

    if requester and requester.lower() != "all":
        filters.append("UPPER(r.name) LIKE UPPER(?)")
        params.append(f"%{requester}%")

    if supplier and supplier.lower() != "all":
        filters.append("UPPER(s.name) LIKE UPPER(?)")
        params.append(f"%{supplier}%")

    if start_date:
        valid_start_date = validate_date(start_date)
        if valid_start_date:
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(valid_start_date)

    if end_date:
        valid_end_date = validate_date(end_date)
        if valid_end_date:
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(valid_end_date)

    if order_number:
        filters.append("o.order_number LIKE ?")
        params.append(f"%{order_number}%")

    where_clause = " AND ".join(filters) if filters else "1=1"

    cursor.execute(f"""
        SELECT
            o.id, o.order_number, o.status, o.created_date, o.received_date, o.total,
            o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
            s.name AS supplier,
            r.name AS requester,
            -- FIX START: Get the user for the LATEST general audit action for the order
            latest_audit_user.username AS audit_user
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        LEFT JOIN requesters r ON o.requester_id = r.id
        LEFT JOIN (
            SELECT at1.order_id, at1.user_id
            FROM audit_trail at1
            JOIN (
                SELECT order_id, MAX(action_date) AS max_date
                FROM audit_trail
                GROUP BY order_id
            ) m ON m.order_id = at1.order_id AND at1.action_date = m.max_date
        ) latest_audit_record ON latest_audit_record.order_id = o.id
        LEFT JOIN users latest_audit_user ON latest_audit_record.user_id = latest_audit_user.id

        -- FIX END
        WHERE {where_clause}
        ORDER BY o.order_number DESC
    """, params)
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

@router.get("/payment_history/{order_id}")
@handle_db_errors(entity="order_payments", action="fetching")
async def get_order_payment_history(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, order_id, amount_paid, payment_date, payment_status, created_at FROM order_payments WHERE order_id = ?", (order_id,))
    rows = cursor.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    log_success("order_payments", "fetched", f"{len(result)} records for order {order_id}")
    return {"payments": result}

# NEW: Endpoint to mark COD payment
@router.put("/mark_cod_paid/{order_id}")
@handle_db_errors(entity="order_payments", action="marking COD paid")
async def mark_cod_paid(order_id: int, payment: CodPayment, request: Request):
    user = request.session.get("user")
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    current_user_id = user["id"]

    # Map frontend payment statuses to database-compatible values
    status_mapping = {
        "Paid": FULLY_PAID,
        "Partially Paid": PARTIALLY_PAID,
    }
    db_payment_status = status_mapping.get(payment.payment_status)
    if not db_payment_status:
        raise HTTPException(status_code=400, detail="Invalid payment status")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verify order exists and is a COD order
        cursor.execute("SELECT total, payment_terms FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order["payment_terms"] != "COD":
            raise HTTPException(status_code=400, detail="Order is not a COD order")

        # Insert payment record into order_payments
        cursor.execute("""
            INSERT INTO order_payments (order_id, amount_paid, payment_date, payment_status, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, payment.amount_paid, payment.payment_date, db_payment_status, current_user_id, now_utc_iso()))

        # Update orders table with payment details
        cursor.execute("""
            UPDATE orders
            SET amount_paid = COALESCE(amount_paid, 0) + ?,
                payment_date = ?,
                status = ?
            WHERE id = ?
        """, (payment.amount_paid, payment.payment_date, db_payment_status, order_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")

        # FIX: Add a log entry for the payment to the audit trail
        audit_details = f"Payment of R{payment.amount_paid:.2f} recorded as '{db_payment_status}'"
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, "COD Payment recorded", audit_details, current_user_id, now_utc_iso()))

        conn.commit()
        log_success("order_payments", "created", f"COD payment recorded for order {order_id}, amount: {payment.amount_paid}")
        return {"success": True, "message": "COD payment recorded successfully"}
    except Exception as e:
        conn.rollback()
        log_error("order_payments", "marking COD paid", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to record COD payment: {str(e)}")
    finally:
        conn.close()