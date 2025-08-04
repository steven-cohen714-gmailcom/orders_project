import logging
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

from backend.utils.db_utils import handle_db_errors, log_success, log_warning, log_error
from backend.utils.order_utils import calculate_order_total
from backend.database import create_order, get_db_connection 
from backend.utils.permissions_utils import require_login 
from .order_queries import validate_date
from backend.utils.send_email import send_email  # Import for COD email

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

# --- Routes ---
@router.post("")
async def create_new_order(order: OrderCreate, request: Request):
    try:
        logging.info(f"🔍 Incoming order: {order}")
        
        user = request.session.get("user")
        if not user or "id" not in user:
            raise HTTPException(status_code=401, detail="User not authenticated")
        current_user_id = user["id"]

        if order.status != "Draft": # This check is likely redundant as this endpoint is for final orders, not drafts.
            for item in order.items:
                if not item.item_code or not item.project or item.qty_ordered <= 0 or item.price <= 0:
                    raise HTTPException(status_code=400, detail="Invalid item: all fields required for non-draft orders")
            total = calculate_order_total([item.dict() for item in order.items])
        else:
            # This path should ideally not be hit for 'Draft' status, as drafts go to /draft_orders endpoint
            total = 0.0  

        initial_status_for_new_order = order.status 
        if order.status != "Draft" and order.auth_band_required is not None:
            pass 

        order_data = {
            "order_number": order.order_number,
            "status": initial_status_for_new_order, 
            "total": total,
            "order_note": order.order_note,
            "note_to_supplier": order.note_to_supplier,
            "supplier_id": order.supplier_id,
            "requester_id": order.requester_id,
            "payment_terms": order.payment_terms,
            "required_auth_band": order.auth_band_required 
        }

        items = [item.dict() for item in order.items]
        
        # FIX: Add 'await' here
        result = await create_order(order_data, items, current_user_id, created_date=order.created_date, draft_id=order.draft_id)
        
        log_success("order", "created", f"Order {order.order_number} with status {order.status} and total R{total}")

        # --- NEW: COD Payment Notification Email Logic for Non-Draft Creation ---
        if order_data["status"] == 'Pending' and order_data["payment_terms"] == 'COD':
            conn = get_db_connection()  # Re-open conn if needed, but ideally reuse
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT order_number, total FROM orders WHERE id = ?
                """, (result["id"],))
                cod_order = cursor.fetchone()

                if cod_order:
                    cursor.execute("""
                        SELECT order_number, total FROM orders 
                        WHERE payment_terms = 'COD' AND status IN ('Pending', 'Authorised')
                    """)
                    pending_cod_orders = cursor.fetchall()

                    cursor.execute("""
                        SELECT username, email FROM users 
                        WHERE can_receive_payment_notifications = 1 AND email IS NOT NULL AND email != ''
                    """)
                    payment_personnel = cursor.fetchall()

                    if payment_personnel:
                        for person in payment_personnel:
                            recipient_email = person['email']
                            subject = f"COD Order {cod_order['order_number']} Now Ready for Payment (R{cod_order['total']:.2f})"
                            
                            body_lines = [
                                f"Dear {person['username']},",
                                "",
                                f"COD Order (Order Number: {cod_order['order_number']}, Total: R{cod_order['total']:.2f}) has been created and is now ready for payment.",
                                "",
                                "Please log in to the system to mark it as paid."
                            ]

                            if pending_cod_orders:
                                body_lines.append("\nHere are other COD orders currently ready for payment:")
                                for p_order in pending_cod_orders:
                                    body_lines.append(f"- Order {p_order['order_number']} (R{p_order['total']:.2f})")
                            else:
                                body_lines.append("\nThere are no other COD orders currently pending payment.")

                            body_lines.append("\nKind regards,\nUniversal Recycling System")
                            email_body = "\n".join(body_lines)

                            try:
                                await send_email(recipient_email, subject, email_body)
                                logging.info(f"COD payment notification email sent to {recipient_email} for new order {result['id']}.")
                            except Exception as email_e:
                                logging.error(f"Failed to send COD payment notification email to {recipient_email} for new order {result['id']}: {email_e}")
                    else:
                        logging.warning(f"No payment personnel found with email for new COD order {result['id']}.")
            except Exception as e:
                logging.error(f"Error in COD email logic for new order {result['id']}: {e}")
            finally:
                conn.close()
        # --- END NEW: COD Payment Notification Email Logic ---

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
    logging.info(f"🔄 Attempting to update draft order ID: {order_id}")
    items = payload.get("items", [])
    if not items:
        logging.warning(f"Draft update for order {order_id}: No items provided in payload. Proceeding with total 0.")
        pass

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch payment_terms before update (for COD check later)
        cursor.execute("SELECT payment_terms FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        payment_terms = row["payment_terms"] if row else None

        # 1. Update order_items with new quantities and prices
        for item in items:
            item_id = item.get("item_id")
            logging.info(f"   - Processing item ID: {item_id} for order {order_id}")
            try:
                qty = float(item.get("quantity", 0))
                price = float(item.get("unit_price", 0))
            except (TypeError, ValueError) as e:
                raise HTTPException(status_code=400, detail=f"Invalid quantity or price format for item ID: {item_id}. Error: {e}")

            if item_id is None:
                raise HTTPException(status_code=400, detail="Missing item_id for an item in draft update payload")

            cursor.execute("""
                UPDATE order_items
                SET qty_ordered = ?, price = ?
                WHERE id = ? AND order_id = ?
            """, (qty, price, item_id, order_id))
            logging.info(f"     - Updated item {item_id}: qty={qty}, price={price}")

        # 2. Get the new calculated total of the order
        cursor.execute("""
            SELECT SUM(oi.qty_ordered * oi.price) AS calculated_total
            FROM order_items oi
            WHERE oi.order_id = ?
        """, (order_id,))
        order_total_result = cursor.fetchone()
        
        new_order_total = order_total_result["calculated_total"] if order_total_result and order_total_result["calculated_total"] is not None else 0.0
        logging.info(f"   - Calculated new_order_total: {new_order_total}")


        # 3. Determine the required_auth_band_id and new status based on the new total and settings thresholds
        new_status = 'Pending' # Default status
        assigned_auth_band_id = None # Default assigned band if no authorization required by amount

        # Fetch all authorization thresholds from settings
        cursor.execute("SELECT auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4, auth_threshold_5 FROM settings WHERE id = 1")
        settings_thresholds = cursor.fetchone()
        logging.info(f"   - Settings thresholds fetched: {settings_thresholds}")

        # Re-indented and corrected logic for authorization thresholds
        if settings_thresholds:
            # Convert thresholds to float, use 0.0 if NULL or not set for comparison
            thresh1 = float(settings_thresholds['auth_threshold_1']) if settings_thresholds and settings_thresholds['auth_threshold_1'] is not None else 0.0
            thresh2 = float(settings_thresholds['auth_threshold_2']) if settings_thresholds and settings_thresholds['auth_threshold_2'] is not None else 0.0
            thresh3 = float(settings_thresholds['auth_threshold_3']) if settings_thresholds and settings_thresholds['auth_threshold_3'] is not None else 0.0
            thresh4 = float(settings_thresholds['auth_threshold_4']) if settings_thresholds and settings_thresholds['auth_threshold_4'] is not None else 0.0
            thresh5 = float(settings_thresholds['auth_threshold_5']) if settings_thresholds and settings_thresholds['auth_threshold_5'] is not None else 0.0 # ADDED

            # Determine the highest band that the new_order_total falls into
            if new_order_total > thresh5: # Check against thresh5 first for "greater than XXX"
                assigned_auth_band_id = 5 # Assign band 5 if greater than threshold 5
            elif new_order_total > thresh4:
                assigned_auth_band_id = 4
            elif new_order_total > thresh3:
                assigned_auth_band_id = 3
            elif new_order_total > thresh2:
                assigned_auth_band_id = 2
            elif new_order_total > thresh1:
                assigned_auth_band_id = 1
            # If new_order_total is <= thresh1, assigned_auth_band_id remains None (no amount-based authorization needed)

            # If an authorization band is determined, set status to Awaiting Authorisation
            if assigned_auth_band_id is not None:
                new_status = 'Awaiting Authorisation'
        else:
            logging.warning("   - No settings thresholds found. Order will default to Pending status.")

        logging.info(f"   - Determined new_status: {new_status}, Assigned auth band ID: {assigned_auth_band_id}")

        # 4. Update the order with the new total, determined status, AND assigned_auth_band_id
        cursor.execute("""
            UPDATE orders
            SET total = ?, status = ?, required_auth_band = ? -- ADDED required_auth_band update
            WHERE id = ? AND status = 'Draft' -- Ensure we only update if it's still a draft
        """, (new_order_total, new_status, assigned_auth_band_id, order_id))

        if cursor.rowcount == 0:
            logging.warning(f"   - Order {order_id} not found or not in 'Draft' status for final update.")
            raise HTTPException(status_code=404, detail="Draft order not found or its status has already changed from 'Draft'.")

        conn.commit()
        log_success("draft_order", "updated", f"Draft order {order_id} submitted as {new_status}", {"user_id": current_user_id}) # Added user_id to log

        # --- NEW: COD Payment Notification Email Logic ---
        if new_status == 'Pending' and payment_terms == 'COD':
            # Fetch order details for the newly submitted COD order
            cursor.execute("""
                SELECT order_number, total FROM orders WHERE id = ?
            """, (order_id,))
            cod_order = cursor.fetchone()

            if cod_order:
                # Fetch other pending COD orders (Pending or Authorised)
                cursor.execute("""
                    SELECT order_number, total FROM orders 
                   WHERE payment_terms = 'COD' AND status IN ('Pending', 'Authorised')
                """)
                pending_cod_orders = cursor.fetchall()

                # Fetch users who should receive notifications
                cursor.execute("""
                    SELECT username, email FROM users 
                    WHERE can_receive_payment_notifications = 1 AND email IS NOT NULL AND email != ''
                """)
                payment_personnel = cursor.fetchall()

                if payment_personnel:
                    for person in payment_personnel:
                        recipient_email = person['email']
                        subject = f"COD Order {cod_order['order_number']} Now Ready for Payment (R{cod_order['total']:.2f})"
                        
                        body_lines = [
                            f"Dear {person['username']},",
                            "",
                            f"COD Order (Order Number: {cod_order['order_number']}, Total: R{cod_order['total']:.2f}) has been submitted and is now ready for payment.",
                            "",
                            "Please log in to the system to mark it as paid."
                        ]

                        if pending_cod_orders:
                            body_lines.append("\nHere are other COD orders currently ready for payment:")
                            for order in pending_cod_orders:
                                body_lines.append(f"- Order {order['order_number']} (R{order['total']:.2f})")
                        else:
                            body_lines.append("\nThere are no other COD orders currently pending payment.")

                        body_lines.append("\nKind regards,\nUniversal Recycling System")
                        email_body = "\n".join(body_lines)

                        try:
                            await send_email(recipient_email, subject, email_body)
                            logging.info(f"COD payment notification email sent to {recipient_email} for order {order_id}.")
                        except Exception as email_e:
                            logging.error(f"Failed to send COD payment notification email to {recipient_email} for order {order_id}: {email_e}")
                else:
                    logging.warning(f"No payment personnel found with email for COD order {order_id}.")
        # --- END NEW: COD Payment Notification Email Logic ---

        return {"message": f"Draft order updated and submitted as {new_status}", "new_total": new_order_total}

    except Exception as e:
        conn.rollback() # Rollback any changes on error
        logging.exception(f"❌ Error updating draft order {order_id} (caught in function's handler): {e}")
        raise HTTPException(status_code=500, detail="Failed to update draft: A server server error occurred.")
    finally:
        conn.close()

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
    return result # frontend expects raw array

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

    filters.append("UPPER(o.status) != 'DELETED'")

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
            -- Subquery to find the user_id for the *absolute latest* audit_trail entry for each order
            SELECT
                at_inner.order_id,
                at_inner.user_id,
                MAX(at_inner.action_date) AS latest_action_date
            FROM audit_trail at_inner
            GROUP BY at_inner.order_id
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