from pathlib import Path

TARGET_FILE = Path("backend/endpoints/orders.py")

receive_route_code = '''
@router.post("/receive")
async def receive_order(payload: dict):
    \"\"\"
    Mark items in an order as received.
    Updates qty_received, status, and received_date if fully received.
    \"\"\"
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
            cursor.execute(\"\"\"
                UPDATE order_items
                SET qty_received = ?
                WHERE order_id = ? AND item_code = ?
            \"\"\", (
                item["qty_received"],
                order_id,
                item["item_code"]
            ))

        # Check if order is fully received
        cursor.execute(\"\"\"
            SELECT qty_ordered, qty_received
            FROM order_items
            WHERE order_id = ?
        \"\"\", (order_id,))
        all_items = cursor.fetchall()

        fully_received = all(
            qty_received is not None and qty_received >= qty_ordered
            for qty_ordered, qty_received in all_items
        )

        if fully_received:
            cursor.execute(\"\"\"
                UPDATE orders
                SET status = 'Received',
                    received_date = ?
                WHERE id = ?
            \"\"\", (datetime.now().isoformat(), order_id))
        conn.commit()
        conn.close()
        return {\"message\": \"Order updated successfully\", \"fully_received\": fully_received}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f\"Database error: {str(e)}\")
'''
if __name__ == "__main__":
    content = TARGET_FILE.read_text()
    insert_point = content.rfind('@router.get')
    updated = content[:insert_point] + receive_route_code.strip() + '\n\n' + content[insert_point:]
    TARGET_FILE.write_text(updated)
    print("✅ /receive route injected.")
