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
    supplier_note: Optional[str] = None
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
            requester_row = cursor.fetchone()
            if not requester_row:
                raise HTTPException(status_code=400, detail="Invalid requester_id")

        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            requester_name = cursor.fetchone()
            result["requester"] = requester_name[0] if requester_name else "Unknown"

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
                       o.order_note, o.supplier_note, r.name AS requester
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
                       o.order_note, o.supplier_note, r.name AS requester
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
            fields = ["Order Number", "Status", "Created Date", "Received Date", "Total", "Order Note", "Supplier Note", "Requester"]
            f.write("\n".join([f"{label}: {value}" for label, value in zip(fields, order)]))
            f.write("\n\nLine Items:\n-----------\n")
            for item in items:
                f.write("\n".join([f"{k}: {v}" for k, v in zip(["Item Code", "Description", "Project", "Qty", "Price", "Total"], item)]))
                f.write("\n\n")

        return {"status": "✅ Order export triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Print failed: {e}")
