# File: backend/database.py
"""
Self-healing SQLite database layer for the Orders system.

- Creates all core tables if missing.
- Adds missing columns safely (SQLite lacks IF NOT EXISTS for columns → try/except).
- Seeds single-row config tables where appropriate.
- Includes Evolution Export schema (batches, settings, per-line flags) idempotently.
- Exposes the same public functions you already call elsewhere.

IMPORTANT:
- This module is STRICTLY data-layer. It does NOT send emails and does NOT dispatch email triggers.
  All email/alert behaviour must be handled in backend/utils/email_and_alerts_engine.py or higher layers.

Public API (unchanged signatures):
- get_db_connection()
- init_db()
- determine_status_and_band(total) -> (status, required_band)   # DEPRECATED: kept for compatibility
- create_order(order_data, items, current_user_id, created_date=None, draft_id=None)  # async
- get_settings() -> dict
- update_settings(payload: dict) -> None
- get_business_details() -> dict
- get_next_requisition_number() -> str
- mark_cod_payment(order_id, amount_paid, payment_date, payment_status) -> None
- log_cod_payment_action(order_id, amount_paid, payment_status, user_id) -> None
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
import logging
from typing import Optional, Tuple, Dict, Any, List

from backend.utils.time_utils import now_utc_iso

# --- Logging ---
Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename="logs/db_activity_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

DB_PATH = Path("data/orders.db")


# -------- Connection helpers --------
def get_db_connection() -> sqlite3.Connection:
    """Open a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Keep default pragmas; don't flip foreign_keys on older DBs unexpectedly.
    return conn


def _add_column_if_missing(cur: sqlite3.Cursor, table: str, column: str, ddl: str) -> None:
    """
    Add a column to a table if it's missing.
    :param ddl: full 'ALTER TABLE <table> ADD COLUMN ...' statement
    """
    try:
        cur.execute(ddl)
        logging.info(f"Added column '{column}' to '{table}'.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            # already there → fine
            pass
        else:
            logging.warning(f"Could not add column '{column}' to '{table}': {e}")


# -------- Schema init (idempotent) --------
def init_db() -> None:
    """
    Initialize DB structures in an idempotent way.
    Creates tables if missing; adds columns via guarded ALTERs; seeds singletons.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            # --- Core master tables ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requesters (
                    id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number      TEXT,
                    name                TEXT,
                    telephone           TEXT,
                    vat_number          TEXT,
                    registration_number TEXT,
                    email               TEXT,
                    contact_name        TEXT,
                    contact_telephone   TEXT,
                    address_line1       TEXT,
                    address_line2       TEXT,
                    address_line3       TEXT,
                    postal_code         TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_number             TEXT,
                    status                   TEXT,
                    created_date             TEXT,
                    received_date            TEXT,
                    total                    REAL,
                    order_note               TEXT,
                    note_to_supplier         TEXT,
                    supplier_id              INTEGER,
                    requester_id             INTEGER,
                    required_auth_band       INTEGER,
                    payment_terms            TEXT DEFAULT 'On account',
                    payment_date             TEXT,
                    amount_paid              REAL,
                    last_modified_by_user_id INTEGER,
                    FOREIGN KEY (supplier_id)  REFERENCES suppliers(id),
                    FOREIGN KEY (requester_id) REFERENCES requesters(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id         INTEGER,
                    item_code        TEXT,
                    item_description TEXT,
                    project          TEXT,
                    qty_ordered      REAL,
                    qty_received     REAL,
                    received_date    TEXT,
                    price            REAL,
                    total            REAL,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id           INTEGER,
                    filename           TEXT NOT NULL,
                    file_path          TEXT NOT NULL,
                    upload_date        TEXT NOT NULL,
                    requisition_id     INTEGER,
                    requisition_number TEXT,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id    INTEGER,
                    action      TEXT,
                    details     TEXT,
                    action_date TEXT,
                    user_id     INTEGER,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    order_number_start   TEXT,
                    auth_threshold_1     INTEGER,
                    auth_threshold_2     INTEGER,
                    auth_threshold_3     INTEGER,
                    auth_threshold_4     INTEGER,
                    auth_threshold_5     INTEGER,
                    requisition_number_start TEXT DEFAULT 'REQ1000'
                )
            """)

            # --- Safety patch: ensure Band-5 is not below Band-4 ---
            cur.execute("SELECT auth_threshold_4, auth_threshold_5 FROM settings WHERE id = 1")
            row = cur.fetchone()
            if row is not None and row["auth_threshold_4"] is not None and row["auth_threshold_5"] is not None:
                try:
                    if float(row["auth_threshold_5"]) < float(row["auth_threshold_4"]):
                        cur.execute("UPDATE settings SET auth_threshold_5 = auth_threshold_4 WHERE id = 1")
                        conn.commit()
                except Exception:
                    # Don't block init on conversion issues
                    pass

            # --- Users (base definition for brand-new DBs) ---
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password_hash TEXT,
                rights TEXT,
                auth_threshold_band INTEGER CHECK (auth_threshold_band IN (1, 2, 3, 4, 5)),
                roles TEXT,
                email TEXT,
                can_receive_payment_notifications INTEGER DEFAULT 0,
                can_receive_review_notifications  INTEGER DEFAULT 0,
                can_delete_transactions           INTEGER DEFAULT 0,
                can_edit_draft_orders             INTEGER DEFAULT 0
            )
        """)

            # Backfill missing user columns (legacy DBs)
            _add_column_if_missing(cur, "users", "email",
                "ALTER TABLE users ADD COLUMN email TEXT")
            _add_column_if_missing(cur, "users", "can_receive_payment_notifications",
                "ALTER TABLE users ADD COLUMN can_receive_payment_notifications INTEGER DEFAULT 0")
            _add_column_if_missing(cur, "users", "can_receive_review_notifications",
                "ALTER TABLE users ADD COLUMN can_receive_review_notifications INTEGER DEFAULT 0")
            _add_column_if_missing(cur, "users", "can_delete_transactions",
                "ALTER TABLE users ADD COLUMN can_delete_transactions INTEGER DEFAULT 0")
            _add_column_if_missing(cur, "users", "can_edit_draft_orders",
                "ALTER TABLE users ADD COLUMN can_edit_draft_orders INTEGER DEFAULT 0")

            # --- Payments table ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS order_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id       INTEGER NOT NULL,
                    amount_paid    REAL    NOT NULL,
                    payment_date   TEXT    NOT NULL,
                    payment_status TEXT    NOT NULL CHECK (payment_status IN ('Fully Paid', 'Partially Paid')),
                    created_by     INTEGER,
                    created_at     TEXT,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            """)

            # --- Projects / Items ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_code TEXT UNIQUE,
                    project_name TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_code TEXT UNIQUE,
                    item_description TEXT
                )
            """)

            # --- Business details (seed once) ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS business_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name  TEXT NOT NULL,
                    address_line1 TEXT,
                    address_line2 TEXT,
                    city          TEXT,
                    province      TEXT,
                    postal_code   TEXT,
                    telephone     TEXT,
                    vat_number    TEXT
                )
            """)
            cur.execute("""
                INSERT OR IGNORE INTO business_details (
                    id, company_name, address_line1, address_line2, city, province,
                    postal_code, telephone, vat_number
                ) VALUES (
                    1, 'Universal Recycling Company Pty Ltd', '123 Industrial Road', 'Unit 4',
                    'Cape Town', 'Western Cape', '8001', '+27 21 555 1234', 'VAT123456789'
                )
            """)

            # --- Requisitions (minimal) ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requisitioners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requisitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_number TEXT UNIQUE,
                    requisitioner_id   INTEGER,
                    requisition_date   TEXT,
                    requisition_note   TEXT,
                    status             TEXT,
                    converted_order_id INTEGER,
                    FOREIGN KEY (requisitioner_id) REFERENCES requisitioners(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requisition_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_id INTEGER,
                    description    TEXT,
                    quantity       REAL,
                    project        TEXT,
                    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requisition_attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requisition_id INTEGER,
                    filename       TEXT,
                    file_path      TEXT,
                    upload_date    TEXT,
                    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
                )
            """)

            # --- Draft orders ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS draft_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_number  TEXT,
                    status        TEXT DEFAULT 'Draft',
                    created_date  TEXT,
                    total         REAL,
                    order_note    TEXT,
                    note_to_supplier TEXT,
                    supplier_id   INTEGER,
                    requester_id  INTEGER,
                    payment_terms TEXT DEFAULT 'On account',
                    last_modified_by_user_id INTEGER,
                    FOREIGN KEY (supplier_id)  REFERENCES suppliers(id),
                    FOREIGN KEY (requester_id) REFERENCES requesters(id),
                    FOREIGN KEY (last_modified_by_user_id) REFERENCES users(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS draft_order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    draft_order_id   INTEGER,
                    item_code        TEXT,
                    item_description TEXT,
                    project          TEXT,
                    qty_ordered      REAL,
                    price            REAL,
                    total            REAL,
                    FOREIGN KEY (draft_order_id) REFERENCES draft_orders(id)
                )
            """)

            # --- Receiving logs (lightweight) ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS received_item_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_item_id       INTEGER NOT NULL,
                    qty_received        REAL    NOT NULL,
                    received_by_user_id INTEGER NOT NULL,
                    received_date       TEXT    NOT NULL
                )
            """)

            # --- Evolution Export schema (idempotent) ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS evo_export_batches (
                  id INTEGER PRIMARY KEY,
                  created_at TEXT,
                  created_by TEXT,
                  filename   TEXT,
                  notes      TEXT,
                  row_count  INTEGER DEFAULT 0
                )
            """)
            _add_column_if_missing(cur, "order_items", "evo_exported",
                "ALTER TABLE order_items ADD COLUMN evo_exported INTEGER DEFAULT 0")
            _add_column_if_missing(cur, "order_items", "evo_export_batch_id",
                "ALTER TABLE order_items ADD COLUMN evo_export_batch_id INTEGER")
            _add_column_if_missing(cur, "order_items", "evo_exported_at",
                "ALTER TABLE order_items ADD COLUMN evo_exported_at TEXT")
            _add_column_if_missing(cur, "order_items", "evo_export_hash",
                "ALTER TABLE order_items ADD COLUMN evo_export_hash TEXT")
            _add_column_if_missing(cur, "users", "can_edit_draft_orders",
                "ALTER TABLE users ADD COLUMN can_edit_draft_orders INTEGER DEFAULT 0")

            cur.execute("UPDATE order_items SET evo_exported = 0 WHERE evo_exported IS NULL")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_evo_exported ON order_items(evo_exported)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_evo_batch     ON order_items(evo_export_batch_id)")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS evo_export_settings (
                  id INTEGER PRIMARY KEY CHECK (id = 1),
                  default_transaction_code  TEXT,
                  default_gl_contra_account TEXT,
                  default_warehouse_code    TEXT,
                  date_format               TEXT,
                  description_template      TEXT,
                  encoding                  TEXT
                )
            """)
            cur.execute("""
                INSERT OR IGNORE INTO evo_export_settings
                  (id, default_transaction_code, default_gl_contra_account, default_warehouse_code, date_format, description_template, encoding)
                VALUES
                  (1, 'JNL', '9999-000', 'MAIN', 'YYYY/MM/DD', 'PO {order_number} – {supplier_name}', 'utf-8')
            """)

            conn.commit()
            logging.info("Database initialized successfully.")

    except sqlite3.Error as e:
        logging.error(f"❌ DB init failed: {e}")
        raise


# -------- Business logic helpers (DEPRECATED here; engines own decisions) --------
def determine_status_and_band(total: float) -> Tuple[str, int]:
    """
    DEPRECATED: band/status computation belongs in the authorisations engine at review-time.
    Kept only for compatibility with older callers. Prefer not to use.
    Returns (status, required_band). If under lowest threshold → Pending / band 0.
    """
    logging.warning("determine_status_and_band called in DB layer (deprecated). "
                    "Move callers to the authorisations engine.")
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT auth_threshold_1, auth_threshold_2, auth_threshold_3,
                   auth_threshold_4, auth_threshold_5
            FROM settings WHERE id = 1
        """)
        row = cur.fetchone()
        if not row:
            raise ValueError("Authorization thresholds not configured in settings.")

        thresholds = [float(row[f"auth_threshold_{i}"]) for i in range(1, 6)]
        status = "Pending"
        required_band = 0

        if total > thresholds[4]:
            status, required_band = "Awaiting Authorisation", 5
        elif total > thresholds[3]:
            status, required_band = "Awaiting Authorisation", 4
        elif total > thresholds[2]:
            status, required_band = "Awaiting Authorisation", 3
        elif total > thresholds[1]:
            status, required_band = "Awaiting Authorisation", 2
        elif total > thresholds[0]:
            status, required_band = "Awaiting Authorisation", 1

        return status, required_band


# -------- Order creation (NO trigger logic here) --------
async def create_order(
    order_data: Dict[str, Any],
    items: List[Dict[str, Any]],
    current_user_id: int,
    created_date: Optional[str] = None,
    draft_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Create an order + items and log audit.
    - Does NOT send emails.
    - Does NOT dispatch trigger events.
    - Always stores new orders as 'For Review' (or 'Draft' if explicitly passed).
    - Banding is NEVER computed at creation time (required_auth_band is stored as NULL).
    """
    # Review-first creation: no band here
    explicit_status = order_data.get("status")
    if explicit_status == "Draft":
        status = "Draft"
    else:
        status = "For Review"

    required_band = None  # never set at creation

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Insert order
        created_ts = created_date or now_utc_iso()
        cur.execute("""
            INSERT INTO orders (
                order_number, status, created_date, total, order_note, note_to_supplier,
                supplier_id, requester_id, required_auth_band, payment_terms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data["order_number"],
            status,
            created_ts,
            float(order_data["total"]),
            order_data.get("order_note"),
            order_data.get("note_to_supplier"),
            int(order_data["supplier_id"]),
            int(order_data["requester_id"]),
            None,  # required_auth_band is NULL at creation
            (order_data.get("payment_terms") or "On account"),
        ))

        order_id = cur.lastrowid

        # Insert items
        for it in items:
            cur.execute("""
                INSERT INTO order_items (
                    order_id, item_code, item_description, project, qty_ordered, price, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                it.get("item_code"),
                it.get("item_description"),
                it.get("project"),
                float(it["qty_ordered"]),
                float(it["price"]),
                float(it["qty_ordered"]) * float(it["price"]),
            ))

        # Audit trail
        if draft_id:
            cur.execute(
                "INSERT INTO audit_trail (order_id, action, details, user_id, action_date) "
                "VALUES (?, 'Converted from Draft', ?, ?, ?)",
                (order_id, f"Order converted from Draft ID: {int(draft_id)}",
                 int(current_user_id), now_utc_iso()),
            )
        else:
            cur.execute(
                "INSERT INTO audit_trail (order_id, action, details, user_id, action_date) "
                "VALUES (?, 'Created', ?, ?, ?)",
                (order_id, f"Order {order_data['order_number']} created",
                 int(current_user_id), now_utc_iso()),
            )

        conn.commit()

        logging.info(
            "Order created (no triggers dispatched here): order_id=%s status='%s' required_band=%s",
            order_id, status, required_band
        )

        # Return created order
        cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        return dict(cur.fetchone())

    except Exception as e:
        conn.rollback()
        logging.error("❌ Error in create_order: %s", e, exc_info=True)
        raise
    finally:
        conn.close()


# -------- Settings / business details --------
def get_settings() -> Dict[str, Any]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT order_number_start, auth_threshold_1, auth_threshold_2,
                   auth_threshold_3, auth_threshold_4, auth_threshold_5, requisition_number_start
            FROM settings WHERE id = 1
        """)
        row = cur.fetchone()
        return dict(row) if row else {}


def update_settings(payload: Dict[str, Any]) -> None:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO settings (
                id, order_number_start, auth_threshold_1, auth_threshold_2,
                auth_threshold_3, auth_threshold_4, auth_threshold_5, requisition_number_start
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                order_number_start       = excluded.order_number_start,
                auth_threshold_1         = excluded.auth_threshold_1,
                auth_threshold_2         = excluded.auth_threshold_2,
                auth_threshold_3         = excluded.auth_threshold_3,
                auth_threshold_4         = excluded.auth_threshold_4,
                auth_threshold_5         = excluded.auth_threshold_5,
                requisition_number_start = excluded.requisition_number_start
        """, (
            1,
            payload["order_number_start"],
            payload["auth_threshold_1"],
            payload["auth_threshold_2"],
            payload["auth_threshold_3"],
            payload["auth_threshold_4"],
            payload["auth_threshold_5"],
            payload.get("requisition_number_start", "REQ1000"),
        ))
        conn.commit()


def get_business_details() -> Dict[str, Any]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, address_line1, address_line2, city, province,
                   postal_code, telephone, vat_number
            FROM business_details WHERE id = 1
        """)
        row = cur.fetchone()
        return dict(row) if row else {}


# -------- Requisition numbering --------
def get_next_requisition_number() -> str:
    """
    Return next requisition number and persist the increment.
    Example: REQ1000 → REQ1001
    """
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT requisition_number_start FROM settings WHERE id = 1")
        row = cur.fetchone()
        if not row:
            raise ValueError("Missing settings row for requisition_number_start. Please configure settings first.")

        current = row["requisition_number_start"]
        prefix = "".join(ch for ch in current if ch.isalpha()) or "REQ"
        digits = "".join(ch for ch in current if ch.isdigit())
        next_num = (int(digits) + 1) if digits else 1000
        new_number = f"{prefix}{next_num}"

        cur.execute("UPDATE settings SET requisition_number_start = ? WHERE id = 1", (new_number,))
        conn.commit()
        return new_number


# -------- COD payments logging --------
def mark_cod_payment(order_id: int, amount_paid: float, payment_date: str, payment_status: str) -> None:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders
               SET amount_paid = ?, payment_date = ?
             WHERE id = ?
        """, (float(amount_paid), payment_date, int(order_id)))
        conn.commit()


def log_cod_payment_action(order_id: int, amount_paid: float, payment_status: str, user_id: int) -> None:
    with get_db_connection() as conn:
        cur = conn.cursor()
        desc = f"COD payment of R{float(amount_paid):.2f} marked as '{payment_status}'"
        cur.execute("""
            INSERT INTO audit_trail (order_id, action, details, user_id, action_date)
            VALUES (?, 'COD Payment', ?, ?, ?)
        """, (int(order_id), desc, int(user_id), now_utc_iso()))
        conn.commit()
