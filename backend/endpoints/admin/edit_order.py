# File: backend/endpoints/admin/edit_order.py

import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

from backend.database import get_db_connection
from backend.utils.db_utils import handle_db_errors, log_success, log_warning, log_error
from backend.utils.order_utils import calculate_order_total
from backend.utils.permissions_utils import require_login, require_screen_permission

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Configure logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- Pydantic Models for Request Body ---
class EditOrderItem(BaseModel):
    id: Optional[int] = None # ID is optional for new items, required for existing ones
    item_code: str
    item_description: Optional[str] = None # Can be derived from item_code lookup
    project: Optional[str] = None
    qty_ordered: float
    price: float

class EditOrderPayload(BaseModel):
    supplier_id: int
    requester_id: int
    payment_terms: str
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    items: List[EditOrderItem]

# --- HTML Route for the Edit Order Page ---
@router.get("/edit_order/{order_id}", response_class=HTMLResponse,
            dependencies=[Depends(require_login), Depends(require_screen_permission("edit_order_admin"))])
async def edit_order_page(request: Request, order_id: int):
    """
    Renders the HTML page for editing an existing order.
    Fetches all necessary data (order details, items, lookups) to populate the form.
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()

        # Fetch order details
        cursor.execute("""
            SELECT o.id, o.order_number, o.status, o.created_date, o.total,
                   o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
                   o.payment_terms, o.last_modified_by_user_id,
                   s.name AS supplier_name, r.name AS requester_name
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN requesters r ON o.requester_id = r.id
            WHERE o.id = ?
        """, (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")

        # Fetch order items
        cursor.execute("""
            SELECT id, item_code, item_description, project, qty_ordered, price, total
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        order_items = [dict(row) for row in cursor.fetchall()]

        # Fetch all lookup data for dropdowns
        cursor.execute("SELECT id, name FROM requesters ORDER BY name")
        requesters = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT id, name, account_number FROM suppliers ORDER BY name")
        suppliers = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT id, item_code, item_description FROM items ORDER BY item_code")
        items = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT id, project_code, project_name FROM projects ORDER BY project_code")
        projects = [dict(row) for row in cursor.fetchall()]

        logger.info(f"Rendering edit_order page for Order ID: {order_id}")
        return templates.TemplateResponse(
            "admin/edit_order.html",
            {
                "request": request,
                "order": dict(order),
                "order_items": order_items,
                "requesters": requesters,
                "suppliers": suppliers,
                "items": items,
                "projects": projects
            }
        )
    except Exception as e:
        logger.exception(f"Error loading edit_order page for Order ID {order_id}")
        raise HTTPException(status_code=500, detail=f"Failed to load order for editing: {str(e)}")
    finally:
        conn.close()

# --- API Route for Updating an Order ---
@router.put("/edit_order/{order_id}",
            # --- FIX START: Changed 'edit_orders_admin' to 'edit_order_admin' ---
            dependencies=[Depends(require_login), Depends(require_screen_permission("edit_order_admin"))])
            # --- FIX END ---
@handle_db_errors(entity="order", action="updating via admin edit")
async def update_order_admin(order_id: int, payload: EditOrderPayload, request: Request):
    """
    Handles the submission of the edited order form.
    Updates main order details and recreates line items.
    """
    user = request.session.get("user")
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    current_user_id = user["id"]
    current_username = user["username"]

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Validate order existence
        cursor.execute("SELECT order_number, status FROM orders WHERE id = ?", (order_id,))
        existing_order = cursor.fetchone()
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found.")

        order_number = existing_order["order_number"]
        old_status = existing_order["status"]

        # 2. Calculate new total from payload items
        new_total = calculate_order_total([item.dict() for item in payload.items])

        # 3. Update main order details
        # Note: Status is NOT changed by this admin edit, it remains as is.
        cursor.execute("""
            UPDATE orders
            SET supplier_id = ?,
                requester_id = ?,
                payment_terms = ?,
                order_note = ?,
                note_to_supplier = ?,
                total = ?,
                last_modified_by_user_id = ?
            WHERE id = ?
        """, (
            payload.supplier_id,
            payload.requester_id,
            payload.payment_terms,
            payload.order_note,
            payload.note_to_supplier,
            new_total,
            current_user_id,
            order_id
        ))

        # 4. Delete existing order items
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))

        # 5. Insert new/updated order items
        for item in payload.items:
            # Fetch item_description if not provided (e.g., if only item_code is sent from frontend)
            item_description = item.item_description
            if not item_description and item.item_code:
                cursor.execute("SELECT item_description FROM items WHERE item_code = ?", (item.item_code,))
                desc_row = cursor.fetchone()
                if desc_row:
                    item_description = desc_row["item_description"]
                else:
                    item_description = "N/A" # Fallback if item code not found in lookup

            cursor.execute("""
                INSERT INTO order_items (
                    order_id, item_code, item_description, project, qty_ordered, price, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                item.item_code,
                item_description,
                item.project,
                item.qty_ordered,
                item.price,
                item.qty_ordered * item.price # Calculate item total
            ))

        # 6. Log to audit trail
        details = (f"Order {order_number} edited by {current_username}. "
                   f"Supplier: {payload.supplier_id}, Requester: {payload.requester_id}, "
                   f"Payment Terms: {payload.payment_terms}, New Total: R{new_total:.2f}. "
                   f"Line items updated.")
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
            VALUES (?, 'Order Edited', ?, ?, ?)
        """, (order_id, details, datetime.now().isoformat(), current_user_id))

        conn.commit()
        log_success("order", "edited", f"Order {order_id} updated by admin {current_username}")
        return {"message": "Order updated successfully"}

    except Exception as e:
        conn.rollback()
        logger.exception(f"Error updating order {order_id} via admin interface")
        raise HTTPException(status_code=500, detail=f"Failed to update order: {str(e)}")
    finally:
        conn.close()