#!/usr/bin/env python3

"""
PURPOSE:
This script resets the orders database by clearing all dynamic data —
including orders, items, projects, suppliers, etc. — while retaining core config tables.

The following tables are preserved:
- users: to retain login/authentication
- settings: to retain order number + threshold config
- requesters: assumed to be manually curated, not imported
- business_details: used for invoice headers and PDF output

All other tables will be wiped (rows deleted), including:
- orders, order_items, audit_trail, attachments
- projects, items, suppliers (to allow fresh CSV import)
- received_item_logs
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# --- Config: Set the path to your database ---
DB_PATH = Path("/Users/stevencohen/Projects/universal_recycling/orders_project/data/orders.db")
BACKUP_DIR = DB_PATH.parent
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_PATH = BACKUP_DIR / f"orders_backup_before_reset_{TIMESTAMP}.db"

# Tables to retain during cleanup
STATIC_TABLES = {
    "users",
    "settings",
    "requesters",
    "business_details"
}

def get_all_tables(conn):
    """
    Return all table names in the database (excluding sqlite internal tables).
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

def clear_non_static_tables(conn, all_tables):
    """
    Delete all data from non-static tables.
    """
    cursor = conn.cursor()
    cleared, skipped = 0, 0

    # Disable foreign keys for clean deletion
    cursor.execute("PRAGMA foreign_keys = OFF;")

    for table in all_tables:
        if table in STATIC_TABLES:
            print(f"⏭️ Skipping static table: {table}")
            skipped += 1
            continue

        # Count and delete rows
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        row_count = cursor.fetchone()[0]
        cursor.execute(f"DELETE FROM {table};")
        print(f"🧹 Cleared {row_count} rows from: {table}")
        cleared += 1

    # Re-enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()

    print(f"\n✅ Cleanup complete: {cleared} tables cleared, {skipped} skipped.")

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
        clear_non_static_tables(conn, tables)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
