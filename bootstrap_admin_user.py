import sqlite3
import bcrypt
from pathlib import Path

# Path to your SQLite DB
DB_PATH = Path("data/universal_orders.db")  # Adjust if your DB is elsewhere

# Admin user config
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # You can change this before running
ADMIN_RIGHTS = "admin"
ADMIN_BAND = 3

def bootstrap_admin():
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (ADMIN_USERNAME,))
    if cursor.fetchone():
        print("✅ Admin user already exists. No changes made.")
        conn.close()
        return

    hashed_pw = bcrypt.hashpw(ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, rights, auth_threshold_band)
            VALUES (?, ?, ?, ?)
        """, (ADMIN_USERNAME, hashed_pw, ADMIN_RIGHTS, ADMIN_BAND))
        conn.commit()
        print("✅ Admin user created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Failed to insert admin user: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    bootstrap_admin()
