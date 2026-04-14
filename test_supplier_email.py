import sys
sys.path.insert(0, '/home/steven_cohen714/orders_project')

from backend.utils.email_and_alerts_engine import send_supplier_notification
from backend.database import get_db_connection

# Find an order with a supplier email
with get_db_connection() as conn:
    conn.row_factory = None
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, o.order_number, s.name, s.email
        FROM orders o
        LEFT JOIN suppliers s ON o.supplier_id = s.id
        WHERE s.email IS NOT NULL AND s.email != ''
        LIMIT 1
    """)
    row = cur.fetchone()

if row:
    order_id, order_number, supplier_name, supplier_email = row
    print(f"Found order: {order_number}")
    print(f"Supplier: {supplier_name}")
    print(f"Email: {supplier_email}")
    print(f"\nSending supplier notification...")

    result = send_supplier_notification(order_id)

    if result:
        print("✅ Supplier notification sent successfully!")
    else:
        print("❌ Failed to send supplier notification")
else:
    print("No orders found with supplier email addresses")
    print("\nLet's update a supplier with a test email address...")

    # Update first supplier with test email
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE suppliers SET email = 'steven.cohen714@gmail.com' WHERE id = 1")
        conn.commit()

    print("✅ Updated supplier 1 with test email")
    print("\nNow find an order from that supplier...")

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, order_number FROM orders WHERE supplier_id = 1 LIMIT 1")
        row = cur.fetchone()

    if row:
        order_id, order_number = row
        print(f"Found order: {order_number}")
        print(f"\nSending supplier notification...")

        result = send_supplier_notification(order_id)

        if result:
            print("✅ Supplier notification sent successfully!")
        else:
            print("❌ Failed to send supplier notification")
    else:
        print("No orders found for supplier 1")
