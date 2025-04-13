import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/orders.db")
cursor = conn.cursor()

# Create high-value order
cursor.execute("""
    INSERT INTO orders (
        order_number, status, created_date, total,
        order_note, supplier_note, requester
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "PO_TEST_002",
    "Awaiting Authorisation",
    datetime.now().isoformat(),
    15000.00,
    "High value test order",
    "Urgent supplier note",
    "Steven"
))
order_id = cursor.lastrowid

# Add line items
items = [
    ("TEST003", "Expensive Valve", "Project Z", 5, 0, 3000.00, 15000.00)
]

for item in items:
    cursor.execute("""
        INSERT INTO order_items (
            order_id, item_code, item_description, project,
            qty_ordered, qty_received, price, total
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_id, *item))

conn.commit()
conn.close()
print("✅ Awaiting Authorisation test order inserted.")
