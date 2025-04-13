import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/orders.db")
cursor = conn.cursor()

# Create order
cursor.execute("""
    INSERT INTO orders (
        order_number, status, created_date, total,
        order_note, supplier_note, requester
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "PO_TEST_001",
    "Pending",
    datetime.now().isoformat(),
    999.99,
    "This is a test order note",
    "This is a supplier note",
    "Steven"
))
order_id = cursor.lastrowid

# Add line items
items = [
    ("TEST001", "Test Widget A", "Project A", 3, 0, 100.00, 300.00),
    ("TEST002", "Test Widget B", "Project B", 2, 0, 349.99, 699.99)
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
print("✅ Test order inserted.")
