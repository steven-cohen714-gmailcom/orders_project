#!/usr/bin/env python3

"""
WARNING: This script performs a FULL RESET of the orders database.

✅ The following tables are preserved:
- users                → Login/authentication
- settings             → Order number + thresholds
- requesters           → Manually curated requesters
- business_details     → Used for invoice headers and PDFs

🧹 The following tables are WIPED (rows deleted):
- orders, order_items
- audit_trail, attachments
- received_item_logs
- suppliers, items, projects → These must be re-imported via CSV after reset

This is typically used when:
- You want to clear ALL transaction data AND imported lookup data
- You're preparing for a fresh CSV import of suppliers/items/projects

A backup of the current DB is created before any data is deleted.
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# --- Config: Update DB path if needed ---
DB_PATH = Path("/Users/stevencohen/Projects/universal_recycling/orders_project/data/orders.db")
BACKUP_DIR = DB_PATH.parent
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_PATH = BACKUP_DIR / f"orders_backup_before_full_reset_{TIMESTAMP}.db"

# Tables to preserve (won’t be touched)
STATIC_TABLES = {
    "users",
    "settings",
    "requesters",
    "business_details"
}

def get_all_tables(conn):
    """
    Returns all user-defined tables in the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

def clear_non_static_tables(conn, all_tables):
    """
    Deletes all rows from every non-static (non-preserved) table.
    """
    cursor = conn.cursor()
    cleared, skipped = 0, 0

    cursor.execute("PRAGMA foreign_keys = OFF;")  # Disable FK constraints temporarily

    for table in all_tables:
        if table in STATIC_TABLES:
            print(f"⏭️ Skipping preserved table: {table}")
            skipped += 1
            continue

        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        row_count = cursor.fetchone()[0]

        cursor.execute(f"DELETE FROM {table};")
        print(f"🧹 Deleted {row_count} rows from: {table}")
        cleared += 1

    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    print(f"\n✅ Reset complete — {cleared} tables cleared, {skipped} preserved.")

def main():
    if not DB_PATH.exists():
        print(f"❌ Database file not found: {DB_PATH}")
        return

    print(f"📦 Backing up current DB to: {BACKUP_PATH}")
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
