from pathlib import Path

TARGET_FILE = Path("backend/endpoints/orders.py")

new_route_code = '''
@router.get("/all")
async def get_all_orders():
    \"\"\"
    Retrieve all orders regardless of status.
    \"\"\"
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(\"\"\"
            SELECT id, order_number, status, created_date, total,
                   order_note, supplier_note, requester
            FROM orders
        \"\"\")

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
'''
if __name__ == "__main__":
    content = TARGET_FILE.read_text()
    insert_point = content.rfind('@router.get')
    updated = content[:insert_point] + new_route_code.strip() + '\n\n' + content[insert_point:]
    TARGET_FILE.write_text(updated)
    print("✅ /all orders route injected.")
