from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

injected_code = '''
@router.get("/print_to_file/{order_id}")
def print_order_to_file(order_id: int):
    import sqlite3
    from pathlib import Path

    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT order_number, status, created_date, received_date, total,
                       order_note, supplier_note, requester
                FROM orders
                WHERE id = ?
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

        output = []
        output.append(f"Order: {order[0]}")
        output.append(f"Status: {order[1]}")
        output.append(f"Created Date: {order[2]}")
        output.append(f"Received Date: {order[3] or 'N/A'}")
        output.append(f"Total: {order[4]}")
        output.append(f"Requester: {order[7]}")
        output.append(f"Order Note: {order[5] or 'None'}")
        output.append(f"Supplier Note: {order[6] or 'None'}")
        output.append("\nLine Items:")
        for item in items:
            output.append(f"  - {item[0]} | {item[1]} | {item[2]} | Qty: {item[3]} | Price: {item[4]} | Total: {item[5]}")

        Path("data/printouts").mkdir(parents=True, exist_ok=True)
        out_path = Path(f"data/printouts/order_{order_id}.txt")
        out_path.write_text("\n".join(output))
        return {"message": f"Order written to {out_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Print failed: {str(e)}")
'''

if __name__ == "__main__":
    text = TARGET.read_text()
    if "def print_order_to_file" in text:
        print("🔁 Route already exists.")
    else:
        insert_index = text.rfind("@router.get")
        updated = text[:insert_index] + injected_code.strip() + "\n\n" + text[insert_index:]
        TARGET.write_text(updated)
        print("✅ /print_to_file/{order_id} route injected.")
