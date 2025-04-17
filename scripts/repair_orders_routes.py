from pathlib import Path

file = Path("backend/endpoints/orders.py")
routes_code = '''from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import sqlite3
from datetime import datetime
from pathlib import Path

router = APIRouter()

@router.get("/all")
def get_all_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {e}")

@router.get("/pending")
def get_pending_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.status = 'Pending'
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"pending_orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending orders: {e}")

@router.get("/print_to_file/{order_id}")
def print_order_to_file(order_id: int):
    output_path = Path("data/printouts") / f"order_{order_id}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            cursor.execute("""
                SELECT * FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = cursor.fetchall()

        lines = [
            f"Order Number: {order['order_number']}",
            f"Status: {order['status']}",
            f"Created: {order['created_date']}",
            f"Requester: {order['requester']}",
            f"Total: {order['total']}",
            f"Supplier Note: {order['supplier_note'] or 'None'}",
            f"Order Note: {order['order_note'] or 'None'}",
            "",
            "Items:"
        ]
        for item in items:
            lines.append(
                f"- {item[2]} | {item[3]} | Qty: {item[4]} | Price: {item[6]} | Total: {item[7]}"
            )

        output_path.write_text("\n".join(lines))
        return {"message": f"Order written to {output_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Print failed: {str(e)}")

@router.post("/receive")
def receive_order(payload: dict):
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        order_id = payload.get("order_id")
        items = payload.get("items", [])

        for item in items:
            cursor.execute("""
                UPDATE order_items
                SET qty_received = ?
                WHERE order_id = ? AND item_code = ?
            """, (
                item["qty_received"],
                order_id,
                item["item_code"]
            ))

        cursor.execute("""
            SELECT qty_ordered, qty_received FROM order_items WHERE order_id = ?
        """, (order_id,))
        all_items = cursor.fetchall()
        fully_received = all(qr is not None and qr >= qo for qo, qr in all_items)

        if fully_received:
            cursor.execute("""
                UPDATE orders SET status = 'Received', received_date = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), order_id))

        conn.commit()
        conn.close()
        return {"message": "Order received", "fully_received": fully_received}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Receive failed: {e}")

@router.get("/audit/{order_id}")
def get_audit(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM audit_trail WHERE order_id = ?
                ORDER BY action_date
            """, (order_id,))
            logs = [dict(row) for row in cursor.fetchall()]
        return {"audit_trail": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit fetch failed: {e}")

@router.post("/upload_attachment")
async def upload_attachment(order_id: int = Form(...), file: UploadFile = File(...)):
    import os
    try:
        folder = Path("data/uploads")
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, file.filename, str(file_path), datetime.now().isoformat()))
            conn.commit()

        return {"message": "Attachment uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
'''

file.write_text(routes_code)
print("✅ backend/endpoints/orders.py replaced with all missing routes.")
