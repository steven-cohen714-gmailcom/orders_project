from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path

from ..database import create_order, get_setting, update_setting
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="frontend/templates")

class OrderItem(BaseModel):
    item_code: str = Field(min_length=1)
    item_description: str = Field(min_length=1)
    project: str = Field(min_length=1)
    qty_ordered: float = Field(gt=0)
    price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.qty_ordered * self.price

class OrderCreate(BaseModel):
    order_number: Optional[str] = None
    requester_id: int = Field(gt=0)
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    items: List[OrderItem] = Field(min_length=1)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

@router.post("")
async def create_new_order(order: OrderCreate):
    try:
        validate_order_items(order.items)
        total = order.total

        auth_threshold = float(get_setting("auth_threshold"))
        current_order_number = get_setting("order_number_start")

        if not order.order_number:
            order.order_number = generate_order_number(current_order_number)
            next_order_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_order_number)

        status = determine_status(total, auth_threshold)

        if total > auth_threshold:
            print(f"[WHATSAPP] Order {order.order_number} exceeds threshold, notify for auth.")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Invalid requester_id")

        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            name_row = cursor.fetchone()
            result["requester"] = name_row[0] if name_row else "Unknown"

        return {"message": "Order created successfully", "order": result}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/all")
def get_all_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.order_number, o.status, o.created_date, o.total,
                       o.order_note, o.note_to_supplier, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                ORDER BY o.created_date DESC
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {e}")

@router.get("/print_to_file/{order_id}")
def print_order_to_file(order_id: int):
    output_path = Path("data/printouts") / f"order_{order_id}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_number, o.status, o.created_date, o.received_date, o.total,
                       o.order_note, o.note_to_supplier, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            cursor.execute("""
                SELECT item_code, item_description, project, qty_ordered, price, total
                FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = cursor.fetchall()

        with output_path.open("w", encoding="utf-8") as f:
            fields = ["Order Number", "Status", "Created Date", "Received Date", "Total", "Order Note", "Note to Supplier", "Requester"]
            f.write("\n".join([f"{label}: {value}" for label, value in zip(fields, order)]))
            f.write("\n\nLine Items:\n-----------\n")
            for item in items:
                f.write("\n".join([f"{k}: {v}" for k, v in zip(["Item Code", "Description", "Project", "Qty", "Price", "Total"], item)]))
                f.write("\n\n")

        return {"status": "✅ Order export triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Print failed: {e}")

@router.get("/pending")
def get_pending_orders(requester_id: Optional[int] = None, supplier_id: Optional[int] = None):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            base_query = """
                SELECT o.id, o.order_number, o.status, o.created_date, o.total,
                       o.order_note, o.note_to_supplier, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.status = 'Pending'
            """
            params = []

            if requester_id:
                base_query += " AND o.requester_id = ?"
                params.append(requester_id)

            if supplier_id:
                base_query += " AND o.supplier_id = ?"
                params.append(supplier_id)

            base_query += " ORDER BY o.created_date DESC"

            cursor.execute(base_query, params)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"pending_orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending orders: {e}")

@router.post("/receive")
def mark_order_received(receive_data: List[dict]):
    try:
        now = datetime.now().isoformat()
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()

            order_ids_updated = set()
            for item in receive_data:
                order_id = item["order_id"]
                item_id = item["item_id"]
                qty_received = item["qty_received"]

                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ? AND order_id = ?
                """, (qty_received, now, item_id, order_id))

                cursor.execute("""
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, 'Received', ?, ?, ?)
                """, (order_id, f"Item ID {item_id} received: {qty_received}", now, 0))

                order_ids_updated.add(order_id)

            for order_id in order_ids_updated:
                cursor.execute("""
                    SELECT COUNT(*) FROM order_items
                    WHERE order_id = ? AND (qty_received IS NULL OR qty_received < qty_ordered)
                """, (order_id,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        UPDATE orders
                        SET status = 'Received', received_date = ?
                        WHERE id = ?
                    """, (now, order_id))

        return {"status": "✅ Order(s) marked as received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to receive order: {e}")

@router.get("/received")
def get_received_orders(requester_id: Optional[int] = None, supplier_id: Optional[int] = None):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            base_query = """
                SELECT o.id, o.order_number, o.status, o.created_date, o.total,
                       o.order_note, o.note_to_supplier, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.status = 'Received'
            """
            params = []

            if requester_id:
                base_query += " AND o.requester_id = ?"
                params.append(requester_id)

            if supplier_id:
                base_query += " AND o.supplier_id = ?"
                params.append(supplier_id)

            base_query += " ORDER BY o.created_date DESC"

            cursor.execute(base_query, params)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"received_orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch received orders: {e}")

@router.get("/audit/{order_id}")
def get_audit_trail(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, action, details, action_date, user_id
                FROM audit_trail
                WHERE order_id = ?
                ORDER BY action_date ASC
            """, (order_id,))
            audit = [dict(row) for row in cursor.fetchall()]
        return {"audit_trail": audit}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch audit trail: {e}")
    
from fastapi import Request
from fastapi.responses import HTMLResponse

@router.get("/new", response_class=HTMLResponse)
def show_new_order_form(request: Request):
    return templates.TemplateResponse("new_order.html", {"request": request})

