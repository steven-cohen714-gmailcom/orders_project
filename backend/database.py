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
            
            # Create requesters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requesters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)

            # Create suppliers table
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

            # Create orders table
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
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                    FOREIGN KEY (requester_id) REFERENCES requesters(id)
                )
            """)

            # Create order_items table
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

            # Create attachments table
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

            # Create audit_trail table
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

            # Create settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password_hash TEXT NOT NULL,
                    rights TEXT NOT NULL
                )
            """)

            # Create projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_code TEXT,
                    project_name TEXT
                )
            """)

            # Create items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_code TEXT,
                    item_description TEXT
                )
            """)

            # Create business_details table
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

            # Insert default business details if not exists
            cursor.execute("""
                INSERT OR IGNORE INTO business_details (
                    id, company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                ) VALUES (
                    1, 'Universal Recycling Company Pty Ltd', '123 Industrial Road', 'Unit 4', 'Cape Town', 'Western Cape', '8001', '+27 21 555 1234', 'VAT123456789'
                )
            """)

            conn.commit()
            logging.info("Database tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Failed to initialize database: {str(e)}")
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
            SELECT id, order_number, status, created_date, total,
                   order_note, note_to_supplier, supplier_id,
                   requester_id, required_auth_band
            FROM orders WHERE id = ?
        """, (order_id,))
        order = cursor.fetchone()
        return dict(order)

def get_setting(key: str) -> str:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else None

def update_setting(key: str, value: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        """, (key, value))
        conn.commit()

def get_business_details() -> dict:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
            FROM business_details WHERE id = 1
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}