#!/usr/bin/env python3

"""
PURPOSE:
This script clears all *dynamic* (transactional) data from the Universal Recycling orders database,
while preserving all core configuration and lookup tables.

Preserved tables:
- users
- settings
- requesters
- business_details
- items
- projects
- suppliers
- requisitioners
- screen_permissions
- sqlite_sequence (this is an internal SQLite table always preserved)

Cleared tables:
- orders
- order_items
- audit_trail
- attachments
- requisitions
- requisition_items
- requisition_attachments
- received_item_logs
- draft_orders (NEWLY ADDED TO CLEARED LIST)
- draft_order_items (NEWLY ADDED TO CLEARED LIST)
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# --- Config: update DB path if needed ---
DB_PATH = Path("/Users/stevencohen/Projects/universal_recycling/orders_project/data/orders.db")
BACKUP_DIR = DB_PATH.parent
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_PATH = BACKUP_DIR / f"orders_backup_before_clear_dynamic_{TIMESTAMP}.db"

# Tables to preserve
STATIC_TABLES = {
    "users",
    "settings",
    "requesters",
    "business_details",
    "items",
    "projects",
    "suppliers",
    "requisitioners",
    "screen_permissions"
}

def get_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Filter out internal SQLite tables and 'sqlite_sequence' which manages AUTOINCREMENT
    return [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

def clear_dynamic_tables(conn, all_tables):
    cursor = conn.cursor()
    cleared_count = 0
    preserved_count = 0
    
    cursor.execute("PRAGMA foreign_keys = OFF;") # Temporarily disable foreign key checks

    for table in all_tables:
        if table in STATIC_TABLES:
            print(f"⏭️ Skipping static table: {table}")
            preserved_count += 1
            continue
        
        # Ensure sqlite_sequence is also skipped, even if not explicitly in STATIC_TABLES set
        if table == "sqlite_sequence":
            print(f"⏭️ Skipping internal SQLite table: {table}")
            preserved_count += 1
            continue

        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            row_count = cursor.fetchone()[0]
            cursor.execute(f"DELETE FROM {table};")
            print(f"🧹 Cleared {row_count} rows from: {table}")
            cleared_count += 1
        except sqlite3.OperationalError as e:
            print(f"❌ Error clearing table {table}: {e}. Skipping.")
            # This might happen if the table was newly added but the script was run on an old DB before init_db()
            # Or if there's a typo in the table name.
            continue


    cursor.execute("PRAGMA foreign_keys = ON;") # Re-enable foreign key checks
    conn.commit()
    print(f"\n✅ Dynamic clear complete: {cleared_count} tables cleared, {preserved_count} preserved.")

def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return

    print(f"📦 Backing up database to: {BACKUP_PATH}")
    shutil.copy2(DB_PATH, BACKUP_PATH)

    print("🔌 Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = get_all_tables(conn)
        clear_dynamic_tables(conn, tables)
    finally:
        conn.close()

if __name__ == "__main__":
    main()