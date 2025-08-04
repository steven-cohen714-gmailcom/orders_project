# File: backend/endpoints/draft_orders.py

import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

from backend.utils.db_utils import handle_db_errors, log_success, log_warning, log_error
from backend.utils.order_utils import calculate_order_total
from backend.database import get_db_connection
from backend.utils.permissions_utils import require_login

router = APIRouter(tags=["draft_orders"])

# --- Models ---
class DraftOrderItemCreate(BaseModel):
    item_code: str
    item_description: str
    project: Optional[str] = None
    qty_ordered: float
    price: float

class DraftOrderCreate(BaseModel):
    order_number: str
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: int
    requester_id: int
    payment_terms: Optional[str] = None
    items: List[DraftOrderItemCreate]

class DraftOrderUpdate(BaseModel):
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    requester_id: Optional[int] = None
    payment_terms: Optional[str] = None
    items: List[DraftOrderItemCreate]


# --- Helper Functions for Database Operations (Specific to Draft Orders) ---
@handle_db_errors(entity="draft_order", action="creating")
async def _insert_draft_order_into_db(order_data: dict, items: list, current_user_id: int) -> dict:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO draft_orders (
                order_number, status, created_date, total, order_note, note_to_supplier,
                supplier_id, requester_id, payment_terms, last_modified_by_user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data["order_number"],
            "Draft",
            datetime.now().isoformat(),
            order_data["total"],
            order_data["order_note"],
            order_data["note_to_supplier"],
            order_data["supplier_id"],
            order_data["requester_id"],
            order_data.get("payment_terms", "On account"),
            current_user_id
        ))
        draft_order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO draft_order_items (
                    draft_order_id, item_code, item_description, project,
                    qty_ordered, price, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                draft_order_id,
                item["item_code"],
                item["item_description"],
                item["project"],
                item["qty_ordered"],
                item["price"],
                item["qty_ordered"] * item["price"]
            ))
        
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id)
            VALUES (?, 'Created as Draft', ?, ?)
        """, (draft_order_id, f"Draft order {order_data['order_number']} created by {current_user_id}", current_user_id))
        
        conn.commit()
        log_success("draft_order", "created", f"Draft order {order_data['order_number']} created with ID {draft_order_id}")
        return {"id": draft_order_id, "order_number": order_data["order_number"]}

@handle_db_errors(entity="draft_order", action="fetching")
async def _get_draft_order_and_items_from_db(draft_id: int) -> dict:
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                do.id, do.order_number, do.status, do.created_date, do.total, 
                do.order_note, do.note_to_supplier, do.supplier_id, do.requester_id,
                do.payment_terms,
                s.name AS supplier_name, r.name AS requester_name
            FROM draft_orders do
            LEFT JOIN suppliers s ON do.supplier_id = s.id
            LEFT JOIN requesters r ON do.requester_id = r.id
            WHERE do.id = ?
        """, (draft_id,))
        draft_order = cursor.fetchone()
        if not draft_order:
            raise HTTPException(status_code=404, detail="Draft order not found")

        cursor.execute("""
            SELECT 
                id, item_code, item_description, project, qty_ordered, price, total
            FROM draft_order_items
            WHERE draft_order_id = ?
        """, (draft_id,))
        items = [dict(row) for row in cursor.fetchall()]

        result = dict(draft_order)
        result["items"] = items
        log_success("draft_order", "fetched", f"Draft order {draft_order['order_number']} (ID: {draft_id}) fetched.")
        return result

@handle_db_errors(entity="draft_order", action="updating")
async def _update_draft_order_in_db(draft_id: int, order_data: dict, items: list, current_user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        update_fields = []
        update_params = []

        if "order_note" in order_data:
            update_fields.append("order_note = ?")
            update_params.append(order_data["order_note"])
        if "note_to_supplier" in order_data:
            update_fields.append("note_to_supplier = ?")
            update_params.append(order_data["note_to_supplier"])
        if "supplier_id" in order_data:
            update_fields.append("supplier_id = ?")
            update_params.append(order_data["supplier_id"])
        if "requester_id" in order_data:
            update_fields.append("requester_id = ?")
            update_params.append(order_data["requester_id"])
        if "payment_terms" in order_data:
            update_fields.append("payment_terms = ?")
            update_params.append(order_data["payment_terms"])
        
        new_total = calculate_order_total(items)
        update_fields.append("total = ?")
        update_params.append(new_total)
        update_fields.append("last_modified_by_user_id = ?")
        update_params.append(current_user_id)
        
        if update_fields:
            cursor.execute(f"""
                UPDATE draft_orders
                SET {', '.join(update_fields)}
                WHERE id = ?
            """, (*update_params, draft_id))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Draft order not found for update.")

        cursor.execute("DELETE FROM draft_order_items WHERE draft_order_id = ?", (draft_id,))
        for item in items:
            cursor.execute("""
                INSERT INTO draft_order_items (
                    draft_order_id, item_code, item_description, project,
                    qty_ordered, price, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                draft_id,
                item["item_code"],
                item["item_description"],
                item["project"],
                item["qty_ordered"],
                item["price"],
                item["qty_ordered"] * item["price"]
            ))

        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id)
            VALUES (?, 'Draft Updated', ?, ?)
        """, (draft_id, f"Draft order {order_data.get('order_number', 'N/A')} updated by {current_user_id}", current_user_id))
        
        conn.commit()
        log_success("draft_order", "updated", f"Draft order {draft_id} updated.")

@handle_db_errors(entity="draft_order", action="deleting")
async def _delete_draft_order_from_db(draft_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM draft_order_items WHERE draft_order_id = ?", (draft_id,))
        cursor.execute("DELETE FROM draft_orders WHERE id = ?", (draft_id,))
        conn.commit()
        log_success("draft_order", "deleted", f"Draft order {draft_id} and its items deleted.")

@handle_db_errors(entity="draft_order", action="fetching list")
async def _get_all_draft_orders_from_db():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                do.id, do.order_number, do.created_date, do.total, do.status,
                s.name AS supplier, r.name AS requester
            FROM draft_orders do
            LEFT JOIN suppliers s ON do.supplier_id = s.id
            LEFT JOIN requesters r ON do.requester_id = r.id
            ORDER BY do.created_date DESC
        """)
        draft_orders = [dict(row) for row in cursor.fetchall()]
        log_success("draft_orders", "fetched list", f"{len(draft_orders)} draft orders retrieved.")
        return draft_orders

# --- Endpoints ---
@router.post("")
async def create_new_draft_order(draft_order: DraftOrderCreate, request: Request):
    user = request.session.get("user")
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    current_user_id = user["id"]

    total = calculate_order_total([item.dict() for item in draft_order.items])

    # CORRECTED SYNTAX: Using string keys for dictionary
    order_data = {
        "order_number": draft_order.order_number,
        "total": total,
        "order_note": draft_order.order_note, # Corrected: "order_note"
        "note_to_supplier": draft_order.note_to_supplier, # Corrected: "note_to_supplier"
        "payment_terms": draft_order.payment_terms,
        "requester_id": draft_order.requester_id,
        "supplier_id": draft_order.supplier_id,
    }
    items_data = [item.dict() for item in draft_order.items]

    result = await _insert_draft_order_into_db(order_data, items_data, current_user_id)
    return {"message": "Draft order created successfully", "draft_id": result["id"], "order_number": result["order_number"]}

@router.get("/pending")
async def get_pending_draft_orders(request: Request):
    
    draft_orders = await _get_all_draft_orders_from_db()
    for order in draft_orders:
        if order["created_date"]:
            try:
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%Y-%m-%d")
            except ValueError:
                order["created_date"] = datetime.strptime(order["created_date"].split(' ')[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        else:
            order["created_date"] = "N/A"
    return {"draft_orders": draft_orders}

@router.get("/{draft_id}")
async def get_draft_order(draft_id: int, request: Request):
    draft_order = await _get_draft_order_and_items_from_db(draft_id)
    return draft_order

@router.put("/{draft_id}")
async def update_draft_order(draft_id: int, draft_order_update: DraftOrderUpdate, request: Request):
    user = request.session.get("user")
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    current_user_id = user["id"]

    order_data = draft_order_update.dict(exclude_unset=True)
    items_data = order_data.pop("items")

    await _update_draft_order_in_db(draft_id, order_data, items_data, current_user_id)
    return {"message": "Draft order updated successfully"}

@router.delete("/{draft_id}")
async def delete_draft_order(draft_id: int, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    await _delete_draft_order_from_db(draft_id)
    return {"message": "Draft order deleted successfully"}

# NEW ENDPOINT: Get items for a specific draft order
@router.get("/api/items/{draft_id}") # Note the /api/ part in the path
@handle_db_errors(entity="draft_order_items", action="fetching")
async def get_items_for_draft_order(draft_id: int):
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id, item_code, item_description, project, qty_ordered, price, total
            FROM draft_order_items
            WHERE draft_order_id = ?
        """, (draft_id,))
        items = [dict(row) for row in cursor.fetchall()]
        log_success("draft_order_items", "fetched", f"{len(items)} items for draft order {draft_id}")
        return items # Return raw array as expected by frontend's expand logic