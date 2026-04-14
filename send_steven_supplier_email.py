import sys
sys.path.insert(0, '/home/steven_cohen714/orders_project')

from backend.utils.email_and_alerts_engine import send_supplier_notification
from backend.database import get_db_connection

# Update supplier 1 temporarily with Steven's email
with get_db_connection() as conn:
    cur = conn.cursor()
    cur.execute("UPDATE suppliers SET email = 'steven.cohen714@gmail.com', contact_name = 'Steven Cohen' WHERE id = 1")
    conn.commit()

print("✅ Updated supplier 1 with Steven's email")

# Find an order from supplier 1
with get_db_connection() as conn:
    conn.row_factory = None
    cur = conn.cursor()
    cur.execute("SELECT id, order_number FROM orders WHERE supplier_id = 1 LIMIT 1")
    row = cur.fetchone()

if row:
    order_id, order_number = row
    print(f"Found order: {order_number}")
    print(f"Sending professional supplier notification to steven.cohen714@gmail.com...")

    result = send_supplier_notification(order_id)

    if result:
        print("✅ Professional supplier notification sent successfully!")
        print("\nCheck your email at steven.cohen714@gmail.com to see the formatted purchase order notification.")
    else:
        print("❌ Failed to send supplier notification")
else:
    print("No orders found for supplier 1")
