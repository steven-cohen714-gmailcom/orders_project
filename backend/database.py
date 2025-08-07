# backend/database.py

import sqlite3
from pathlib import Path
import logging
from typing import Optional
from datetime import datetime
from backend.utils.send_email import send_email

# Logging setup
logging.basicConfig(
    filename="logs/db_activity_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

DB_PATH = Path("data/orders.db")

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_db():
    """
    Initializes the database by creating tables if they don't already exist.
    It also handles schema alterations for the 'users' table and inserts
    default business details if not present.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True) # Ensure the data directory exists
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # --- Core Tables (No Changes Here) ---
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
                    last_modified_by_user_id INTEGER,
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
                    requisition_id INTEGER,
                    requisition_number TEXT,
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
                    auth_threshold_5 INTEGER,
                    requisition_number_start TEXT DEFAULT 'REQ1000'
                )
            """)

            
            # --- MODIFIED: users table to match .schema (no UNIQUE NOT NULL for username) ---
            # This makes the CREATE TABLE statement align with your existing DB's non-enforced state.
            # Ideal: should be UNIQUE NOT NULL, but for "working now" this matches current DB.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,             -- Removed UNIQUE NOT NULL
                    password_hash TEXT,        -- Removed NOT NULL
                    rights TEXT,               -- Removed NOT NULL
                    auth_threshold_band INTEGER CHECK (auth_threshold_band IN (1, 2, 3, 4, 5)),
                    roles TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    amount_paid REAL NOT NULL,
                    payment_date TEXT NOT NULL,
                    payment_status TEXT NOT NULL CHECK (payment_status IN ('Fully Paid', 'Not Fully Paid')),
                    created_by INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (created_by) REFERENCES users(id)
                );
            """)

            # --- Schema Alterations for 'users' table (Add columns if they don't exist) ---
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
                logging.info("Added 'email' column to 'users' table.")
            except sqlite3.OperationalError as e:
                if "duplicate column name: email" not in str(e):
                    logging.warning(f"Could not add 'email' column to 'users' table: {e}")
            
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN can_receive_payment_notifications INTEGER DEFAULT 0")
                logging.info("Added 'can_receive_payment_notifications' column to 'users' table.")
            except sqlite3.OperationalError as e:
                if "duplicate column name: can_receive_payment_notifications" not in str(e):
                    logging.warning(f"Could not add 'can_receive_payment_notifications' column to 'users' table: {e}")
            # --- End Schema Alterations ---

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

            # --- MODIFIED: Requisition Tables matching your .schema output for constraints ---
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
                    requisitioner_id INTEGER, -- Removed NOT NULL as per your .schema
                    requisition_date TEXT,    -- Removed DEFAULT CURRENT_TIMESTAMP as per your .schema
                    requisition_note TEXT,
                    status TEXT,              -- Removed DEFAULT 'submitted' as per your .schema
                    converted_order_id INTEGER,
                    FOREIGN KEY (requisitioner_id) REFERENCES requisitioners(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requisition_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_id INTEGER, -- Removed NOT NULL as per your .schema
                    description TEXT,       -- Removed NOT NULL as per your .schema
                    quantity REAL,
                    project TEXT,           -- ADDED: Project column as per your current .schema
                    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requisition_attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_id INTEGER,
                    filename TEXT,
                    file_path TEXT,
                    upload_date TEXT,
                    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
                )
            """)
            # --- End MODIFIED Requisition Tables ---

            # --- Draft Order Tables (No Changes Here) ---
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS draft_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_number TEXT,
                    status TEXT DEFAULT 'Draft', -- Always 'Draft' for this table
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    total REAL,
                    order_note TEXT,
                    note_to_supplier TEXT,
                    supplier_id INTEGER,
                    requester_id INTEGER,
                    payment_terms TEXT DEFAULT 'On account',
                    last_modified_by_user_id INTEGER, -- To track who last saved the draft
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                    FOREIGN KEY (requester_id) REFERENCES requesters(id),
                    FOREIGN KEY (last_modified_by_user_id) REFERENCES users(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS draft_order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    draft_order_id INTEGER,
                    item_code TEXT,
                    item_description TEXT,
                    project TEXT,
                    qty_ordered REAL,
                    price REAL,
                    total REAL, -- Pre-calculated total for the item
                    FOREIGN KEY (draft_order_id) REFERENCES draft_orders(id)
                )
            """)

            # --- MODIFIED: received_item_logs foreign key references (matching your .schema) ---
            # Your .schema output showed NO REFERENCES for received_item_logs.
            # This makes the FKs NOT enforced by the table itself at creation.
            # For "working now", we align with the schema you provided.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS received_item_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_item_id INTEGER NOT NULL,
                    qty_received REAL NOT NULL,
                    received_by_user_id INTEGER NOT NULL,
                    received_date TEXT NOT NULL
                    -- FOREIGN KEY (order_item_id) REFERENCES order_items(id), -- Removed as per your .schema
                    -- FOREIGN KEY (received_by_user_id) REFERENCES users(id) -- Removed as per your .schema
                )
            """)
            # --- End MODIFIED received_item_logs ---

            conn.commit()
            logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"❌ DB init failed: {e}")
        raise

def determine_status_and_band(total: float) -> tuple[str, int]:
    """
    Determines the authorization status and required band based on the order total
    and configured thresholds.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4, auth_threshold_5 FROM settings WHERE id = 1")
        row = cursor.fetchone()
        if not row:
            raise ValueError("Authorization thresholds not configured in settings.")
        
        # Unpack thresholds and ensure they are floats for comparison
        thresholds = [float(row[f"auth_threshold_{i}"]) for i in range(1, 6)]
        
        status = "Pending" # Default status if no authorization is required
        required_band = 0 # Default band

        # Determine the required authorization band
        if total > thresholds[4]:
            status = "Awaiting Authorisation"
            required_band = 5
        elif total > thresholds[3]:
            status = "Awaiting Authorisation"
            required_band = 4
        elif total > thresholds[2]:
            status = "Awaiting Authorisation"
            required_band = 3
        elif total > thresholds[1]:
            status = "Awaiting Authorisation"
            required_band = 2
        elif total > thresholds[0]:
            status = "Awaiting Authorisation"
            required_band = 1
            
        return status, required_band

async def create_order(order_data: dict, items: list, current_user_id: int, created_date: Optional[str] = None, draft_id: Optional[int] = None) -> dict:
    """
    Creates a new order and its associated items. Handles status determination,
    audit trail logging, and sends email notifications for authorization or COD payments.
    """
    # Determine the order status and required authorization band
    status, required_band = None, None 
    if order_data.get("status") == "Draft":
        status = "Draft"
        required_band = None # Drafts don't require immediate authorization
    else:
        status, required_band = determine_status_and_band(order_data["total"])

    conn = get_db_connection() # Get connection to use across try-finally for atomicity
    try:
        cursor = conn.cursor()
        
        # Insert the order into the 'orders' table
        if created_date:
            # Use provided created_date if available (e.g., when converting a draft that retains its original date)
            cursor.execute("""
                INSERT INTO orders (
                    order_number, status, created_date, total, order_note, note_to_supplier,
                    supplier_id, requester_id, required_auth_band, payment_terms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data["order_number"],
                status,
                created_date,
                order_data["total"],
                order_data["order_note"],
                order_data["note_to_supplier"],
                order_data["supplier_id"],
                order_data["requester_id"],
                required_band,
                order_data.get("payment_terms", "On account")
            ))
        else:
            # Otherwise, let the database set CURRENT_TIMESTAMP
            cursor.execute("""
                INSERT INTO orders (
                    order_number, status, total, order_note, note_to_supplier,
                    supplier_id, requester_id, required_auth_band, payment_terms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data["order_number"],
                status,
                order_data["total"],
                order_data["order_note"],
                order_data["note_to_supplier"],
                order_data["supplier_id"],
                order_data["requester_id"],
                required_band,
                order_data.get("payment_terms", "On account")
            ))

        order_id = cursor.lastrowid # Get the ID of the newly created order

        # Insert order items
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
                item["qty_ordered"] * item["price"] # Calculate item total
            ))
        
        # Audit trail logging
        if draft_id:
            # Log 'Converted from Draft' if the order originated from a draft
            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, user_id)
                VALUES (?, 'Converted from Draft', ?, ?)
            """, (order_id, f"Order converted from Draft ID: {draft_id}", current_user_id))
        else:
            # Otherwise, log 'Created' as usual
            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, user_id)
                VALUES (?, 'Created', ?, ?)
            """, (order_id, f"Order {order_data['order_number']} created", current_user_id))

        conn.commit() # Commit all database changes (order, items, audit trail)

        # --- Email notifications for authorizers ---
        if status == "Awaiting Authorisation" and required_band is not None:
            cursor.execute("""
                SELECT username, email FROM users 
                WHERE auth_threshold_band >= ? AND email IS NOT NULL AND email != ''
            """, (required_band,)) # Select users with sufficient authorization band and an email
            authorizers = cursor.fetchall()

            if authorizers:
                cursor.execute("""
                    SELECT order_number, total FROM orders 
                    WHERE status = 'Awaiting Authorisation' AND required_auth_band >= ?
                """, (required_band,))
                pending_orders_for_band = cursor.fetchall()

                for authorizer in authorizers:
                    recipient_email = authorizer['email']
                    subject = f"New Order {order_data['order_number']} Awaiting Your Authorization (R{order_data['total']:.2f})"
                    
                    body_lines = [
                        f"Dear {authorizer['username']},",
                        "",
                        f"The Universal Recycling Orders System has a new order (Order Number: {order_data['order_number']}, Total: R{order_data['total']:.2f}) for you to authorize.",
                        f"It requires authorization band {required_band}.",
                        "",
                        "There are also " + str(len(pending_orders_for_band) - 1 if pending_orders_for_band else 0) + " other orders that need your authorization.",
                        "",
                        "Please click here to log in and review:",
                        "http://localhost:8004/orders/authorisations_per_user", # Direct link to authorizations screen
                        "",
                        "Kind regards,",
                        "Universal Recycling System"
                    ]

                    if len(pending_orders_for_band) > 1:
                        body_lines.append("\nOther orders awaiting your authorization:")
                        for pending_order in pending_orders_for_band:
                            if pending_order['order_number'] != order_data['order_number']:
                                body_lines.append(f"- Order {pending_order['order_number']} (R{pending_order['total']:.2f})")
                    
                    email_body = "\n".join(body_lines)

                    try:
                        await send_email(recipient_email, subject, email_body)
                        logging.info(f"Authorization email sent to {recipient_email} for order {order_id}.")
                    except Exception as email_e:
                        logging.error(f"Failed to send authorization email to {recipient_email} for order {order_id}: {email_e}")
            else:
                logging.warning(f"No authorizers found with email for band {required_band} for order {order_id}.")
        # --- End Email notifications for authorizers ---

        # --- Email notifications for COD payment personnel (if order is COD and does NOT require authorization) ---
        if order_data.get("payment_terms") == "COD" and status == "Pending": # 'Pending' status implies no authorization required (or already handled)
            cursor.execute("""
                SELECT username, email FROM users 
                WHERE can_receive_payment_notifications = 1 AND email IS NOT NULL AND email != ''
            """)
            payment_personnel = cursor.fetchall()

            if payment_personnel:
                cursor.execute("""
                    SELECT order_number, total FROM orders 
                    WHERE status = 'Pending' AND payment_terms = 'COD'
                """)
                pending_cod_orders = cursor.fetchall()

                for person in payment_personnel:
                    recipient_email = person['email']
                    subject = f"New COD Order {order_data['order_number']} Ready for Payment (R{order_data['total']:.2f})"
                    
                    body_lines = [
                        f"Dear {person['username']},",
                        "",
                        f"The Universal Recycling Orders System has a new COD order (Order Number: {order_data['order_number']}, Total: R{order_data['total']:.2f}) that is now ready for payment.",
                        "",
                        "There are also " + str(len(pending_cod_orders) - 1 if pending_cod_orders else 0) + " other COD orders that need your attention.",
                        "",
                        "Please click here to log in and review:",
                        "http://localhost:8004/orders/cod_orders", # Direct link to COD orders screen
                        "",
                        "Kind regards,",
                        "Universal Recycling System"
                    ]
                    
                    if len(pending_cod_orders) > 1:
                        body_lines.append("\nOther COD orders ready for payment:")
                        for cod_order in pending_cod_orders:
                            if cod_order['order_number'] != order_data['order_number']:
                                body_lines.append(f"- Order {cod_order['order_number']} (R{cod_order['total']:.2f})")

                    email_body = "\n".join(body_lines)

                    try:
                        await send_email(recipient_email, subject, email_body)
                        logging.info(f"COD payment notification email sent to {recipient_email} for order {order_id}.")
                    except Exception as email_e:
                        logging.error(f"Failed to send COD payment notification email to {recipient_email} for order {order_id}: {email_e}")
            else:
                logging.warning(f"No payment personnel found with email for COD order {order_id}.")
        # --- End Email notifications for COD payment personnel ---

        # Retrieve and return the newly created order
        cursor.execute("""
            SELECT * FROM orders WHERE id = ?
        """, (order_id,))
        return dict(cursor.fetchone())

    except Exception as e:
        conn.rollback() # Rollback all changes if any error occurs
        logging.error(f"❌ Error in create_order or sending email notification: {e}", exc_info=True)
        raise
    finally:
        conn.close() # Ensure the database connection is closed

def get_settings() -> dict:
    """Retrieves the application's global settings."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_number_start, auth_threshold_1, auth_threshold_2,
                   auth_threshold_3, auth_threshold_4, auth_threshold_5, requisition_number_start
            FROM settings WHERE id = 1
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}

def update_settings(payload: dict):
    """Updates the application's global settings."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (
                id, order_number_start, auth_threshold_1, auth_threshold_2,
                auth_threshold_3, auth_threshold_4, auth_threshold_5, requisition_number_start
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                order_number_start = excluded.order_number_start,
                auth_threshold_1 = excluded.auth_threshold_1,
                auth_threshold_2 = excluded.auth_threshold_2,
                auth_threshold_3 = excluded.auth_threshold_3,
                auth_threshold_4 = excluded.auth_threshold_4,
                auth_threshold_5 = excluded.auth_threshold_5,
                requisition_number_start = excluded.requisition_number_start
        """, (
            1, # Settings table is designed to have a single row with ID 1
            payload["order_number_start"],
            payload["auth_threshold_1"],
            payload["auth_threshold_2"],
            payload["auth_threshold_3"],
            payload["auth_threshold_4"],
            payload["auth_threshold_5"],
            payload.get("requisition_number_start", "REQ1000")
        ))
        conn.commit()

def get_business_details() -> dict:
    """Retrieves the stored business details."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, address_line1, address_line2, city, province,
                   postal_code, telephone, vat_number
            FROM business_details WHERE id = 1
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}

def get_next_requisition_number():
    """
    Generates and increments the next requisition number based on the
    configured starting number in settings.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT requisition_number_start FROM settings WHERE id = 1")
        row = cursor.fetchone()
        if not row:
            raise ValueError("Missing settings row for requisition_number_start. Please configure settings first.")

        current_number = row["requisition_number_start"]
        # Extract alphabetic prefix and numeric part
        prefix = ''.join(filter(str.isalpha, current_number)) or "REQ" # Default to "REQ" if no alpha
        numeric = ''.join(filter(str.isdigit, current_number))
        
        # Increment the numeric part, defaulting to 1000 if no number found
        next_number = int(numeric) + 1 if numeric else 1000
        new_number = f"{prefix}{next_number}"

        # Update the settings with the new next requisition number
        cursor.execute("UPDATE settings SET requisition_number_start = ? WHERE id = 1", (new_number,))
        conn.commit()
        return new_number

def mark_cod_payment(order_id, amount_paid, payment_date, payment_status):
    """
    Updates an order with COD payment details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE orders
        SET amount_paid = ?, payment_date = ?, payment_status = ?
        WHERE id = ?
    """, (amount_paid, payment_date, payment_status, order_id))
    conn.commit()
    conn.close()


def log_cod_payment_action(order_id: int, amount_paid: float, payment_status: str, user_id: int):
    """
    Logs a COD payment action to the audit trail.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    description = f"COD payment of R{amount_paid:.2f} marked as '{payment_status}'"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO audit_trail (order_id, user_id, action_type, description, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, user_id, "COD Payment", description, timestamp))

    conn.commit()
    conn.close()