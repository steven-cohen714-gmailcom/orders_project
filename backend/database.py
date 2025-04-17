import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any, List

DB_PATH = "data/orders.db"


def init_db() -> None:
    """Create all tables (if they don’t exist) and seed default settings."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # 1. Requesters lookup
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        # 2. Suppliers lookup
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            name TEXT,
            telephone TEXT,
            vat_number TEXT,
            registration_number TEXT,
            email TEXT,
            contact_name TEXT,
            contact_telephone TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            address_line3 TEXT,
            postal_code TEXT
        )
        """)

        # 3. Orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT,
            status TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            received_date TEXT,
            total REAL,
            order_note TEXT,
            note_to_supplier TEXT,
            supplier_id INTEGER REFERENCES suppliers(id),
            requester_id INTEGER REFERENCES requesters(id)
        )
        """)

        # 4. Order items
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            item_code TEXT,
            item_description TEXT,
            project TEXT,
            qty_ordered REAL,
            price REAL,
            total REAL
        )
        """)

        # 5. Attachments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TEXT NOT NULL
        )
        """)

        # 6. Audit trail
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            action TEXT,
            details TEXT,
            action_date TEXT DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER
        )
        """)

        # 7. Settings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # Seed default settings
        cursor.execute(
            "INSERT OR IGNORE INTO settings (key,value) VALUES ('auth_threshold','10000')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO settings (key,value) VALUES ('order_number_start','PO001')"
        )

        conn.commit()


def create_order(order_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Insert a new order and its items, then return the newly created order row as a dict.
    Expects order_data to include:
      - order_number, status, total, order_note (opt), note_to_supplier (opt),
        supplier_id (opt), requester_id (required)
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (
                order_number, status, created_date, total,
                order_note, note_to_supplier, supplier_id, requester_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data["order_number"],
            order_data["status"],
            datetime.now().isoformat(),
            order_data["total"],
            order_data.get("order_note"),
            order_data.get("note_to_supplier"),
            order_data.get("supplier_id"),
            order_data["requester_id"]
        ))
        order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id, item_code, item_description, project,
                    qty_ordered, price, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                item["item_code"],
                item["item_description"],
                item["project"],
                item["qty_ordered"],
                item["price"],
                item["qty_ordered"] * item["price"]
            ))

        conn.commit()

        # Fetch and return the created order row
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        cols = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(cols, row))


def get_setting(key: str) -> Optional[str]:
    """Retrieve a setting’s value, or None if missing."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None


def update_setting(key: str, value: str) -> None:
    """Upsert a setting (insert or update)."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, value))
        conn.commit()
