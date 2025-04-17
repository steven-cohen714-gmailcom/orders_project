from pathlib import Path

file = Path("backend/endpoints/orders.py")
text = file.read_text()

if "order_items = cursor.fetchall()" in text:
    fixed_line = '''
            columns = [desc[0] for desc in cursor.description]
            order_items = [dict(zip(columns, row)) for row in cursor.fetchall()]
    '''
    updated = text.replace("order_items = cursor.fetchall()", fixed_line.strip())
    file.write_text(updated)
    print("✅ print_order now returns dicts instead of tuples.")
else:
    print("❌ Could not find original fetchall() line. No changes made.")
