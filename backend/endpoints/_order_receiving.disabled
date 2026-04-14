# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/order_receiving.py

from fastapi import APIRouter, HTTPException, Request, Depends # Added Request
from datetime import datetime
import sqlite3
from pathlib import Path
import json
from pydantic import BaseModel
from typing import List, Dict

from backend.utils.permissions_utils import require_login # Added import for require_login

router = APIRouter(tags=["orders"])

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

class ReceivedItem(BaseModel):
    item_id: int
    received_qty: float

class ReceivePayload(BaseModel):
    receipt_date: str  # From user input on frontend
    items: List[ReceivedItem]

@router.post("/receive/{order_id}", response_model=dict)
async def receive_order(order_id: int, payload: ReceivePayload, request: Request, user: Dict = Depends(require_login)): # Added request and user dependency
    items = payload.items
    receipt_date = payload.receipt_date  # e.g., "2025-05-13"

    # Get the current user's ID from the session
    current_user_id = user["id"] # Use the user ID from the dependency

    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
            status_row = cursor.fetchone()
            if not status_row:
                raise HTTPException(status_code=404, detail="Order not found")

            order_status = status_row["status"]
            if order_status not in ("Pending", "Authorised", "Partially Received", "Paid"):
                raise HTTPException(
                    status_code=403,
                   detail=f"Order must be 'Pending', 'Authorised', 'Partially Received', or 'Paid' before receiving. Current status: {order_status}"
                )

            all_fully_received = True

            for item in items:
                item_id = item.item_id
                qty_received = item.received_qty

                cursor.execute("""
                    SELECT qty_ordered, qty_received
                    FROM order_items
                    WHERE id = ? AND order_id = ?
                """, (item_id, order_id))
                row = cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

                qty_ordered = row["qty_ordered"]
                current_qty_received = row["qty_received"] or 0
                new_qty_received = current_qty_received + qty_received

                if new_qty_received > qty_ordered:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Received quantity for item {item_id} exceeds ordered quantity"
                    )

                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ?
                """, (new_qty_received, receipt_date, item_id))

                cursor.execute("""
                    INSERT INTO received_item_logs (order_item_id, qty_received, received_by_user_id, received_date)
                    VALUES (?, ?, ?, ?)
                """, (item_id, qty_received, current_user_id, receipt_date)) # CHANGED: Use current_user_id

                if new_qty_received < qty_ordered:
                    all_fully_received = False

            new_status = "Received" if all_fully_received else "Partially Received"
            cursor.execute("""
                UPDATE orders
                SET status = ?, received_date = ?
                WHERE id = ?
            """, (new_status, receipt_date, order_id))

            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Received', ?, ?, ?)
            """, (
                order_id,
                f"Order received: {json.dumps([i.dict() for i in items])}",
                datetime.now().isoformat(),
                current_user_id # CHANGED: Use current_user_id
            ))

            conn.commit()

            log_event("order_receiving_log.txt", {
                "action": "receive",
                "order_id": order_id,
                "items": [i.dict() for i in items],
                "status": new_status,
                "receipt_date": receipt_date,
                "user_id": current_user_id # Log the user ID
            })

            return {"message": "Order received successfully", "status": new_status}

    except sqlite3.Error as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "general"})
        raise HTTPException(status_code=500, detail=f"Failed to receive order: {str(e)}")