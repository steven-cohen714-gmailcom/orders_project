import sqlite3
from pathlib import Path

DB_PATH = Path("/Users/stevencohen/Projects/universal_recycling/orders_project/data/orders.db")

def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

    for table in tables:
        print(f"\n📄 Table: {table}")
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            print(" | ".join(columns))
            print("-" * 50)
            for row in rows:
                print(" | ".join(str(item) for item in row))
        except Exception as e:
            print(f"⚠️ Could not read table {table}: {e}")

    conn.close()

if __name__ == "__main__":
    main()
