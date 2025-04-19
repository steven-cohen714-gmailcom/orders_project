import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

DB_PATH = "data/orders.db"
LOG_PATH = Path("logs/db_activity_log.txt")

def log_db_event(action: str, payload: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {action}: {json.dumps(payload, ensure_ascii=False)}\n")

def init_db() -> None:
    """Create tables and seed default settings."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requesters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )""")

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
                )""")

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
                )""")

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
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    upload_date TEXT NOT NULL
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    action TEXT,
                    details TEXT,
                    action_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )""")

            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('auth_threshold', '10000')"
            )
            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('order_number_start', 'PO001')"
            )

            conn.commit()
            log_db_event("init_db", {"status": "success"})
    except Exception as e:
        log_db_event("init_db_error", {"error": str(e)})
        raise


def create_order(order_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
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

            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]

            log_db_event("create_order", {
                "order_number": order_data["order_number"],
                "requester_id": order_data["requester_id"],
                "total": order_data["total"],
                "items_count": len(items)
            })

            return dict(zip(columns, row))
    except Exception as e:
        log_db_event("create_order_error", {"error": str(e)})
        raise


def get_setting(key: str) -> Optional[str]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            log_db_event("get_setting", {"key": key, "result": row[0] if row else None})
            return row[0] if row else None
    except Exception as e:
        log_db_event("get_setting_error", {"key": key, "error": str(e)})
        raise


def update_setting(key: str, value: str) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """, (key, value))
            conn.commit()
            log_db_event("update_setting", {"key": key, "value": value})
    except Exception as e:
        log_db_event("update_setting_error", {"key": key, "error": str(e)})
        raise
