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
    items: List[ReceivedItem]

@router.post("/receive/{order_id}", response_model=dict)
async def receive_order(order_id: int, payload: ReceivePayload):
    items = payload.items

    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Order not found")
            
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
                
                current_qty_received = row["qty_received"] or 0
                qty_ordered = row["qty_ordered"]
                new_qty_received = current_qty_received + qty_received
                
                if new_qty_received > qty_ordered:
                    raise HTTPException(status_code=400, detail=f"Received quantity for item {item_id} exceeds ordered quantity")
                
                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ?
                """, (new_qty_received, datetime.now().isoformat(), item_id))
                
                if new_qty_received < qty_ordered:
                    all_fully_received = False
            
            new_status = "Received" if all_fully_received else "Partially Received"
            cursor.execute("""
                UPDATE orders
                SET status = ?, received_date = ?
                WHERE id = ?
            """, (new_status, datetime.now().isoformat(), order_id))
            
            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Received', ?, ?, ?)
            """, (order_id, f"Order received: {json.dumps([i.dict() for i in items])}", datetime.now().isoformat(), 0))
            
            conn.commit()
            
            log_event("order_receiving_log.txt", {
                "action": "receive",
                "order_id": order_id,
                "items": [i.dict() for i in items],
                "status": new_status
            })
            
            return {"message": "Order received successfully", "status": new_status}
    except sqlite3.Error as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "general"})
        raise HTTPException(status_code=500, detail=f"Failed to receive order: {str(e)}")

@router.post("/mark_complete/{order_id}", response_model=dict)
async def mark_order_complete(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Order not found")
                
            cursor.execute("""
                UPDATE orders
                SET status = 'Partially Delivered - Accepted'
                WHERE id = ?
            """, (order_id,))
            
            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Marked Complete', ?, ?, ?)
            """, (order_id, f"Order marked as complete with partial delivery", datetime.now().isoformat(), 0))
            
            conn.commit()
            
            log_event("order_receiving_log.txt", {
                "action": "mark_complete",
                "order_id": order_id,
                "status": "Partially Delivered - Accepted"
            })
            
            return {"message": "Order marked as complete"}
    except sqlite3.Error as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        log_event("order_receiving_log.txt", {"error": str(e), "type": "general"})
        raise HTTPException(status_code=500, detail=f"Failed to mark order as complete: {str(e)}")
