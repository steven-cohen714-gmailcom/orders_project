import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# --- Correct DB Path ---
DB_PATH = Path("/Users/stevencohen/Projects/universal_recycling/orders_project/data/orders.db")
BACKUP_DIR = DB_PATH.parent
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_PATH = BACKUP_DIR / f"orders_backup_before_reset_{TIMESTAMP}.db"

# --- Tables to retain ---
STATIC_TABLES = {
    "users", "settings", "requesters", "suppliers",
    "projects", "items", "business_details"
}

def get_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

def clear_non_static_tables(conn, all_tables):
    cursor = conn.cursor()
    for table in all_tables:
        if table not in STATIC_TABLES:
            print(f"🧹 Clearing table: {table}")
            cursor.execute(f"DELETE FROM {table};")
    conn.commit()

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
        print("✅ Non-static tables cleared successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
