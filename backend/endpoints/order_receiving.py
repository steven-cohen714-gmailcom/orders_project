from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import sqlite3
from pathlib import Path  # Add this import
import json

router = APIRouter(prefix="/orders", tags=["orders"])

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

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