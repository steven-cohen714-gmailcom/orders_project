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

Cleared tables:
- orders, order_items, audit_trail, attachments
- received_item_logs

Before wiping any data, a timestamped backup is created.
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# --- Config: path to your live database ---
DB_PATH = Path("/Users/stevencohen/Projects/universal_recycling/orders_project/data/orders.db")
BACKUP_DIR = DB_PATH.parent
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_PATH = BACKUP_DIR / f"orders_backup_before_clear_dynamic_{TIMESTAMP}.db"

# Tables to retain
STATIC_TABLES = {
    "users",
    "settings",
    "requesters",
    "business_details",
    "items",
    "projects",
    "suppliers"
}

def get_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

def clear_dynamic_tables(conn, all_tables):
    cursor = conn.cursor()
    cleared, skipped = 0, 0
    cursor.execute("PRAGMA foreign_keys = OFF;")

    for table in all_tables:
        if table in STATIC_TABLES:
            print(f"⏭️ Skipping static table: {table}")
            skipped += 1
            continue
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        row_count = cursor.fetchone()[0]
        cursor.execute(f"DELETE FROM {table};")
        print(f"🧹 Cleared {row_count} rows from: {table}")
        cleared += 1

    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    print(f"\n✅ Cleanup complete: {cleared} tables cleared, {skipped} preserved.")

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
