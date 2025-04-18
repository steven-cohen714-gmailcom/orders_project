#!/usr/bin/env python3
import sqlite3

DB_PATH = "data/orders.db"

TABLES_TO_CLEAR = [
    "orders",
    "order_items",
    "attachments",
    "audit_trail"
]

def clear_live_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for table in TABLES_TO_CLEAR:
                print(f"Clearing table: {table}")
                cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print("✅ Live transactional data cleared successfully.")
    except Exception as e:
        print(f"❌ Failed to clear data: {e}")

if __name__ == "__main__":
    clear_live_data()

