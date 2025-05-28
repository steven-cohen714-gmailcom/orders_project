import sqlite3
from pathlib import Path
import logging

# Logging setup
logging.basicConfig(
    filename="logs/db_activity_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

DB_PATH = Path("data/orders.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # -- Core Tables --
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requesters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )
            """)
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
                    supplier_id INTEGER,
                    requester_id INTEGER,
                    required_auth_band INTEGER,
                    payment_terms TEXT DEFAULT 'On account',
                    payment_date TEXT,
                    amount_paid REAL,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                    FOREIGN KEY (requester_id) REFERENCES requesters(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    item_code TEXT,
                    item_description TEXT,
                    project TEXT,
                    qty_ordered REAL,
                    qty_received REAL,
                    received_date TEXT,
                    price REAL,
                    total REAL,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    upload_date TEXT NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    action TEXT,
                    details TEXT,
                    action_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    order_number_start TEXT,
                    auth_threshold_1 INTEGER,
                    auth_threshold_2 INTEGER,
                    auth_threshold_3 INTEGER,
                    auth_threshold_4 INTEGER,
                    requisition_number_start TEXT DEFAULT 'REQ1000'
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    rights TEXT NOT NULL,
                    auth_threshold_band INTEGER CHECK (auth_threshold_band IN (1, 2, 3, 4)),
                    roles TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_code TEXT UNIQUE,
                    project_name TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_code TEXT UNIQUE,
                    item_description TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    address_line1 TEXT,
                    address_line2 TEXT,
                    city TEXT,
                    province TEXT,
                    postal_code TEXT,
                    telephone TEXT,
                    vat_number TEXT
                )
            """)
            cursor.execute("""
                INSERT OR IGNORE INTO business_details (
                    id, company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                ) VALUES (
                    1, 'Universal Recycling Company Pty Ltd', '123 Industrial Road', 'Unit 4', 'Cape Town', 'Western Cape', '8001', '+27 21 555 1234', 'VAT123456789'
                )
            """)

            # -- New: Requisitions --
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requisitioners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requisitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_number TEXT UNIQUE,
                    requisitioner_id INTEGER NOT NULL,
                    requisition_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    requisition_note TEXT,
                    status TEXT DEFAULT 'submitted',
                    converted_order_id INTEGER DEFAULT NULL,
                    FOREIGN KEY (requisitioner_id) REFERENCES requisitioners(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requisition_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    project TEXT,
                    quantity REAL,
                    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
                )
            """)

            conn.commit()
            logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"❌ DB init failed: {e}")
        raise

def determine_status_and_band(total: float) -> tuple[str, int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4 FROM settings WHERE id = 1")
        row = cursor.fetchone()
        if not row:
            raise ValueError("Authorization thresholds not configured.")
        thresholds = [row["auth_threshold_1"], row["auth_threshold_2"], row["auth_threshold_3"], row["auth_threshold_4"]]
        status = "Pending"
        required_band = 0
        if total > thresholds[0]:
            status = "Awaiting Authorisation"
            if total <= thresholds[1]:
                required_band = 1
            elif total <= thresholds[2]:
                required_band = 2
            elif total <= thresholds[3]:
                required_band = 3
            else:
                required_band = 4
        return status, required_band

def create_order(order_data: dict, items: list) -> dict:
    status, required_band = determine_status_and_band(order_data["total"])
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (
                order_number, status, total, order_note, note_to_supplier,
                supplier_id, requester_id, required_auth_band
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data["order_number"],
            status,
            order_data["total"],
            order_data["order_note"],
            order_data["note_to_supplier"],
            order_data["supplier_id"],
            order_data["requester_id"],
            required_band
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
        cursor.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id)
            VALUES (?, 'Created', ?, ?)
        """, (order_id, f"Order {order_data['order_number']} created", 0))
        conn.commit()
        cursor.execute("""
            SELECT * FROM orders WHERE id = ?
        """, (order_id,))
        return dict(cursor.fetchone())

def get_settings() -> dict:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_number_start, auth_threshold_1, auth_threshold_2,
                   auth_threshold_3, auth_threshold_4, requisition_number_start
            FROM settings WHERE id = 1
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}

def update_settings(payload: dict):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (
                id, order_number_start, auth_threshold_1, auth_threshold_2,
                auth_threshold_3, auth_threshold_4, requisition_number_start
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                order_number_start = excluded.order_number_start,
                auth_threshold_1 = excluded.auth_threshold_1,
                auth_threshold_2 = excluded.auth_threshold_2,
                auth_threshold_3 = excluded.auth_threshold_3,
                auth_threshold_4 = excluded.auth_threshold_4,
                requisition_number_start = excluded.requisition_number_start
        """, (
            1,
            payload["order_number_start"],
            payload["auth_threshold_1"],
            payload["auth_threshold_2"],
            payload["auth_threshold_3"],
            payload["auth_threshold_4"],
            payload.get("requisition_number_start", "REQ1000")
        ))
        conn.commit()

def get_business_details() -> dict:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, address_line1, address_line2, city, province,
                   postal_code, telephone, vat_number
            FROM business_details WHERE id = 1
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}
