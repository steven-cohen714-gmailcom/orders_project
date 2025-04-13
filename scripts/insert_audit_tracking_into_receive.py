from pathlib import Path

TARGET_FILE = Path("backend/endpoints/orders.py")

audit_block = """
        # Insert into audit trail
        for item in received_items:
            cursor.execute(\"\"\"
                INSERT INTO audit_trail (
                    order_id, action, details, action_date, user_id
                ) VALUES (?, ?, ?, ?, ?)
            \"\"\", (
                order_id,
                'Received',
                f\"Item {item['item_code']} marked as received (qty: {item['qty_received']})\",
                datetime.now().isoformat(),
                1  # Placeholder user_id = 1 (Steven)
            ))
"""

if __name__ == "__main__":
    text = TARGET_FILE.read_text()

    # Inject after the last cursor.execute in receive route (before checking if fully received)
    insert_point = text.find("        # Check if order is fully received")
    if insert_point == -1:
        print("❌ Could not locate insert point. Aborting.")
        exit(1)

    updated = text[:insert_point] + audit_block + "\n" + text[insert_point:]
    TARGET_FILE.write_text(updated)
    print("✅ Audit trail injection complete.")
