# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/order_receiving.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
import sqlite3
from pathlib import Path
import json
from pydantic import BaseModel
from typing import List

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
async def receive_order(order_id: int, payload: ReceivePayload):
    items = payload.items
    receipt_date = payload.receipt_date  # e.g., "2025-05-13"

    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
            status_row = cursor.fetchone()
            if not status_row:
                raise HTTPException(status_code=404, detail="Order not found")

            order_status = status_row["status"]
            # MODIFIED: Include 'Paid' status as an allowed status for receiving.
            if order_status not in ("Pending", "Authorised", "Partially Received", "Paid"):
                raise HTTPException(
                    status_code=403,
                   detail=f"Order must be 'Pending', 'Authorised', 'Partially Received', or 'Paid' before receiving. Current status: {order_status}"
                )

            all_fully_received = True

            for item in items:
                item_id = item.item_id
                qty_received = item.received_qty

                # Fetch existing values
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

                # Update order_items summary
                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ?
                """, (new_qty_received, receipt_date, item_id))

                # Insert detailed record into received_item_logs
                cursor.execute("""
                    INSERT INTO received_item_logs (order_item_id, qty_received, received_by_user_id, received_date)
                    VALUES (?, ?, ?, ?)
                """, (item_id, qty_received, 0, receipt_date))  # TODO: Replace 0 with real user_id when available

                if new_qty_received < qty_ordered:
                    all_fully_received = False

            # Update overall order status
            new_status = "Received" if all_fully_received else "Partially Received"
            # If the original status was 'Paid', and it's not fully received, it should probably stay 'Paid' and become 'Partially Received'
            # (or perhaps 'Partially Received & Paid'). For this task, we'll keep it simple and align with existing transitions.
            # If the order was Paid, and now fully received, new_status becomes 'Received'. If partially received, it becomes 'Partially Received'.
            # This implicitly means the 'Paid' flag is assumed to be carried through.
            cursor.execute("""
                UPDATE orders
                SET status = ?, received_date = ?
                WHERE id = ?
            """, (new_status, receipt_date, order_id))

            # Log audit trail entry
            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Received', ?, ?, ?)
            """, (
                order_id,
                f"Order received: {json.dumps([i.dict() for i in items])}",
                datetime.now().isoformat(),
                0  # TODO: replace with logged-in user
            ))

            conn.commit()

            log_event("order_receiving_log.txt", {
                "action": "receive",
                "order_id": order_id,
                "items": [i.dict() for i in items],
                "status": new_status,
                "receipt_date": receipt_date
            })

            return {"message": "Order received successfully", "status": new_status}

    except sqlite3.Error as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "general"})
        raise HTTPException(status_code=500, detail=f"Failed to receive order: {str(e)}")