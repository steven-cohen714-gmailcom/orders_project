#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = "data/orders.db"

# Transactional tables to clear (excluding static tables: requesters, suppliers, settings, users, projects, items)
TABLES_TO_CLEAR = [
    "orders",
    "order_items",
    "attachments",
    "audit_trail"
]

def clear_transactional_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for table in TABLES_TO_CLEAR:
                print(f"Clearing table: {table}")
                cursor.execute(f"DELETE FROM {table}")
            # Reset the sqlite_sequence for the cleared tables
            for table in TABLES_TO_CLEAR:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table,))
            # Reset the order_number_start to URC0001
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('order_number_start', 'URC0001')")
            conn.commit()
            print("✅ Transactional data cleared successfully. Order number reset to URC0001.")
    except Exception as e:
        print(f"❌ Failed to clear transactional data: {e}")

if __name__ == "__main__":
    # Ensure the uploads directory is cleared as well
    UPLOAD_DIR = Path("data/uploads")
    if UPLOAD_DIR.exists():
        for file in UPLOAD_DIR.glob("*"):
            try:
                file.unlink()
                print(f"Deleted upload: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
    clear_transactional_data()