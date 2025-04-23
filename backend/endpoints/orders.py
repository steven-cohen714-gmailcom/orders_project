from fastapi import APIRouter, HTTPException, Request, UploadFile, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import json
import shutil

from ..database import create_order, get_setting, update_setting
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="frontend/templates")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.get("/next_order_number")
def get_next_order_number():
    try:
        current_number = get_setting("order_number_start")
        next_number = generate_order_number(current_number)
        return {"next_order_number": next_number}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "next_order_number"})
        raise HTTPException(status_code=500, detail=f"Failed to get next order number: {e}")

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
    note_to_supplier: Optional[str] = Field(None, max_length=1000)
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
            next_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_number)

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

        log_event("new_orders_log.txt", {"action": "submit_attempt", "order_data": order_data})

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            name_row = cursor.fetchone()
            result["requester"] = name_row[0] if name_row else "Unknown"

        log_event("new_orders_log.txt", {"action": "submit_success", "order_number": order.order_number, "status": status})

        return {"message": "Order created successfully", "order": result}
    except sqlite3.Error as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "value"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "unexpected"})
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

class ItemReceive(BaseModel):
    order_id: int
    item_id: int
    qty_received: float = Field(gt=0)

@router.post("/receive")
def mark_order_received(receive_data: List[ItemReceive]):
    try:
        now = datetime.now().isoformat()
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            order_ids_updated = set()

            for item in receive_data:
                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ? AND order_id = ?
                """, (item.qty_received, now, item.item_id, item.order_id))

                cursor.execute("""
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, 'Received', ?, ?, ?)
                """, (
                    item.order_id,
                    f"Item ID {item.item_id} received: {item.qty_received}",
                    now,
                    0
                ))

                order_ids_updated.add(item.order_id)

            for order_id in order_ids_updated:
                cursor.execute("""
                    SELECT COUNT(*) FROM order_items
                    WHERE order_id = ? AND (qty_received IS NULL OR qty_received < qty_ordered)
                """, (order_id,))
                incomplete = cursor.fetchone()[0]
                if incomplete == 0:
                    cursor.execute("""
                        UPDATE orders SET status = 'Received', received_date = ?
                        WHERE id = ?
                    """, (now, order_id))

        log_event("new_orders_log.txt", {"action": "receive", "orders": list(order_ids_updated)})
        return {"status": "✅ Order(s) marked as received"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "receive"})
        raise HTTPException(status_code=500, detail=f"Failed to receive order(s): {e}")

@router.post("/upload_attachment")
async def upload_attachment(file: UploadFile, order_id: int = Form(...)):
    try:
        # Validate order_id exists
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Invalid order_id")

        # Sanitize filename and handle duplicates
        filename = file.filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
        base_filename = filename
        saved_path = UPLOAD_DIR / f"{order_id}_{filename}"
        counter = 1
        while saved_path.exists():
            name, ext = base_filename.rsplit(".", 1) if "." in base_filename else (base_filename, "")
            filename = f"{name}_{counter}.{ext}" if ext else f"{name}_{counter}"
            saved_path = UPLOAD_DIR / f"{order_id}_{filename}"
            counter += 1

        # Check file size before saving
        content = await file.read()
        file_size = len(content)
        if file_size < 500:
            raise HTTPException(status_code=400, detail="Uploaded file is too small or corrupt.")

        # Save the file
        with saved_path.open("wb") as buffer:
            buffer.write(content)

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, filename, str(saved_path), datetime.now().isoformat()))
            conn.commit()

        log_event("new_orders_log.txt", {
            "action": "attachment_uploaded",
            "order_id": order_id,
            "filename": filename,
            "path": str(saved_path),
            "size_bytes": file_size
        })

        return {"status": "✅ Attachment uploaded"}
    except sqlite3.Error as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_upload"})
        raise HTTPException(status_code=500, detail=f"Database error during upload: {str(e)}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "upload"})
        raise HTTPException(status_code=500, detail=f"Failed to upload attachment: {str(e)}")
    finally:
        await file.close()

@router.get("/attachments/{order_id}")
def get_order_attachments(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, filename, file_path, upload_date
                FROM attachments
                WHERE order_id = ?
            """, (order_id,))
            files = [dict(row) for row in cursor.fetchall()]
        return {"attachments": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve attachments: {e}")

@router.post("/save_note/{order_id}")
async def save_order_note(order_id: int, data: dict):
    try:
        order_note = data.get("order_note")
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders
                SET order_note = ?
                WHERE id = ?
            """, (order_note, order_id))
            conn.commit()

            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Note Updated', ?, ?, ?)
            """, (order_id, f"Order note updated to: {order_note}", datetime.now().isoformat(), 0))

        log_event("new_orders_log.txt", {"action": "note_updated", "order_id": order_id, "order_note": order_note})
        return {"status": "✅ Order note updated"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "save_note"})
        raise HTTPException(status_code=500, detail=f"Failed to save order note: {e}")

@router.get("/api/orders/pending_orders")
def get_pending_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = []
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        # Always include orders that are either Pending or Awaiting Authorisation
        filters.append("o.status IN ('Pending', 'Waiting for Approval', 'Awaiting Authorisation')")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        if status and status != "All":
            filters.append("o.status = ?")
            params.append(status)

        where_clause = " AND ".join(filters)

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                orders.append(order)
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": where_clause, "params": params})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "pending_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load pending orders: {e}")

@router.get("/api/received_orders")
def get_received_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None)
):
    try:
        filters = ["o.status = 'Received'"]
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        where_clause = " AND ".join(filters)

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                orders.append(order)
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": where_clause, "params": params})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load received orders: {e}")

@router.get("/api/items_for_order/{order_id}")
def get_items_for_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date, price,
                       (qty_ordered * price) AS total
                FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {e}")

@router.get("/api/audit_trail")
def get_audit_trail(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = []
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        if status and status != "All":
            filters.append("o.status = ?")
            params.append(status)

        where_clause = " AND ".join(filters) if filters else "1=1"

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.received_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                if order["received_date"]:
                    order["received_date"] = datetime.fromisoformat(order["received_date"]).strftime("%d/%m/%Y")
                # Fetch items for this order
                cursor.execute("""
                    SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date
                    FROM order_items
                    WHERE order_id = ?
                """, (order["id"],))
                items = [dict(item_row) for item_row in cursor.fetchall()]
                for item in items:
                    if item["received_date"]:
                        item["received_date"] = datetime.fromisoformat(item["received_date"]).strftime("%d/%m/%Y")
                order["items"] = items
                orders.append(order)
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": where_clause, "params": params})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail: {e}")