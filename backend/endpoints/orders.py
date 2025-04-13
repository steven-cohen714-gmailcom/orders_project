from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3

from ..database import create_order, get_setting, update_setting
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items

router = APIRouter(prefix="/orders", tags=["orders"])

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
    requester: str = Field(min_length=1)
    order_note: Optional[str] = None
    supplier_note: Optional[str] = None
    supplier_id: Optional[int] = None
    items: List[OrderItem] = Field(min_length=1)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

@router.post("")
async def create_new_order(order: OrderCreate):
    """
    Create a new purchase order.
    Args:
        order: OrderCreate model containing order details and items
    Returns:
        Created order with items and status
    Raises:
        HTTPException: For database errors or validation failures
    """
    try:
        # Validate order items
        validate_order_items(order.items)

        # Calculate total
        total = order.total

        # Get settings
        auth_threshold = float(get_setting("auth_threshold"))
        current_order_number = get_setting("order_number_start")

        # Generate order number if not provided
        if not order.order_number:
            order.order_number = generate_order_number(current_order_number)
            # Generate the next order number and update settings
            next_order_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_order_number)

        # Determine status based on total
        status = determine_status(total, auth_threshold)

        if total > auth_threshold:
            # 🔔 Placeholder: Send Twilio WhatsApp notification to authorisers
            # from ..integrations.whatsapp import notify_authorisers
            # notify_authorisers(order_number=order.order_number, amount=total)
            print(f"[WHATSAPP] Order {order.order_number} exceeds threshold, notify for auth.")

        # Prepare order data
        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        # Create order and items in database
        result = create_order(
            order_data=order_data,
            items=[item.model_dump() for item in order.items]
        )

        # Format the date in response
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        return {
            "message": "Order created successfully",
            "order": result
        }

    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/all")
async def get_all_orders():
    """
    Retrieve all orders regardless of status.
    """
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, order_number, status, created_date, total,
                   order_note, supplier_note, requester
            FROM orders
        """)

        orders = cursor.fetchall()
        conn.close()

        result = []
        for order in orders:
            result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "status": order["status"],
                "created_date": datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y"),
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"]
            })

        return {"orders": result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/receive")
async def receive_order(payload: dict):
    """
    Mark items in an order as received.
    Updates qty_received, status, and received_date if fully received.
    """
    import sqlite3
    from datetime import datetime

    order_id = payload.get("order_id")
    received_items = payload.get("items", [])

    if not order_id or not received_items:
        raise HTTPException(status_code=400, detail="Missing order_id or items.")

    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()

        # Update each item's qty_received
        for item in received_items:
            cursor.execute("""
                UPDATE order_items
                SET qty_received = ?
                WHERE order_id = ? AND item_code = ?
            """, (
                item["qty_received"],
                order_id,
                item["item_code"]
            ))


        # Insert into audit trail
        for item in received_items:
            cursor.execute("""
                INSERT INTO audit_trail (
                    order_id, action, details, action_date, user_id
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                order_id,
                'Received',
                f"Item {item['item_code']} marked as received (qty: {item['qty_received']})",
                datetime.now().isoformat(),
                1  # Placeholder user_id = 1 (Steven)
            ))

        # Check if order is fully received
        cursor.execute("""
            SELECT qty_ordered, qty_received
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        all_items = cursor.fetchall()

        fully_received = all(
            qty_received is not None and qty_received >= qty_ordered
            for qty_ordered, qty_received in all_items
        )

        if fully_received:
            cursor.execute("""
                UPDATE orders
                SET status = 'Received',
                    received_date = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), order_id))
        conn.commit()
        conn.close()
        return {"message": "Order updated successfully", "fully_received": fully_received}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/audit/{order_id}")
async def get_audit_trail(order_id: int):
    """Retrieve audit trail entries for a given order."""
    import sqlite3
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT action, details, action_date
            FROM audit_trail
            WHERE order_id = ?
            ORDER BY action_date
        """, (order_id,))
        logs = cursor.fetchall()
        conn.close()
        return {"audit_trail": [dict(row) for row in logs]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

from fastapi import UploadFile, File, Form
import os

@router.post("/upload_attachment")
async def upload_attachment(order_id: int = Form(...), file: UploadFile = File(...)):
    """
    Upload an attachment and link it to an order.
    Saves file to data/uploads and logs entry to DB.
    """
    import sqlite3
    from datetime import datetime

    # Create upload folder if it doesn't exist
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = file.filename
    filepath = os.path.join(upload_dir, filename)

    # Save file to disk
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Log in DB
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attachments (
                order_id, filename, file_path, upload_date
            ) VALUES (?, ?, ?, ?)
        """, (order_id, filename, filepath, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return {"message": "Attachment uploaded", "filename": filename}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

from fastapi import UploadFile, File, Form
import os

@router.post("/upload_attachment")
async def upload_attachment(order_id: int = Form(...), file: UploadFile = File(...)):
    """
    Upload an attachment and link it to an order.
    Saves file to data/uploads and logs entry to DB.
    """
    import sqlite3
    from datetime import datetime

    # Create upload folder if it doesn't exist
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = file.filename
    filepath = os.path.join(upload_dir, filename)

    # Save file to disk
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Log in DB
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attachments (
                order_id, filename, file_path, upload_date
            ) VALUES (?, ?, ?, ?)
        """, (order_id, filename, filepath, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return {"message": "Attachment uploaded", "filename": filename}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("")
async def create_new_order(order: OrderCreate):
    from ..database import create_order, get_setting, update_setting
    from ..utils.order_utils import generate_order_number, determine_status, validate_order_items
    import sqlite3
    from datetime import datetime

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
            # 🔔 Placeholder: Send Twilio WhatsApp notification to authorisers
            # from ..integrations.whatsapp import notify_authorisers
            # notify_authorisers(order_number=order.order_number, amount=total)
            print(f"[WHATSAPP] Order {order.order_number} exceeds threshold, notify for auth.")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO requesters (name) VALUES (?)", (order.requester,))
            conn.commit()

        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        return {"message": "Order created successfully", "order": result}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/next_order_number")
async def get_next_order_number():
    from ..database import get_setting
    current = get_setting("order_number_start")
    return {"next_order_number": current}

@router.get("/pending")
async def get_pending_orders():
    """
    Retrieve all pending orders, each with full item breakdown.
    """
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                o.id, o.order_number, o.created_date, o.total,
                o.order_note, o.supplier_note, o.requester
            FROM orders o
            WHERE o.status = 'Pending'
        """)

        orders = cursor.fetchall()
        full_result = []

        for order in orders:
            cursor.execute("""
                SELECT 
                    item_code, item_description, project,
                    qty_ordered, qty_received, price, total
                FROM order_items
                WHERE order_id = ?
            """, (order["id"],))
            items = [dict(row) for row in cursor.fetchall()]
            
            full_result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "created_date": datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y"),
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"],
                "items": items
            })

        conn.close()
        return {"pending_orders": full_result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")