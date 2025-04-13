from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

audit_route = '''
@router.get("/audit/{order_id}")
async def get_audit_trail(order_id: int):
    \"\"\"Retrieve audit trail entries for a given order.\"\"\"
    import sqlite3
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(\"\"\"
            SELECT action, details, action_date
            FROM audit_trail
            WHERE order_id = ?
            ORDER BY action_date
        \"\"\", (order_id,))
        logs = cursor.fetchall()
        conn.close()
        return {"audit_trail": [dict(row) for row in logs]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
'''
if __name__ == "__main__":
    text = TARGET.read_text()
    insert_point = text.rfind('@router.get')
    updated = text[:insert_point] + audit_route.strip() + '\n\n' + text[insert_point:]
    TARGET.write_text(updated)
    print("✅ /audit/{order_id} route injected.")
