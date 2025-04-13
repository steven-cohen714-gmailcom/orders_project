import os
import sqlite3
from contextlib import contextmanager
from typing import Dict, Any, List
from datetime import datetime

@contextmanager
def get_db(db_name: str = "data/orders.db"):
    """
    Context manager for database connections.
    Args:
        db_name: Database file path (default: data/orders.db)
    Ensures proper handling of connections and automatic closing.
    """
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_setting(key: str, db_name: str = "data/orders.db") -> Any:
    """
    Retrieve a setting value from the settings table.
    Args:
        key: The setting key to retrieve
        db_name: Database file path
    Returns:
        The setting value
    """
    with get_db(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result['value'] if result else None

def update_setting(key: str, value: Any, db_name: str = "data/orders.db") -> None:
    """
    Update a setting value in the settings table.
    Args:
        key: The setting key to update
        value: The new value
        db_name: Database file path
    """
    with get_db(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
        conn.commit()

def create_order(order_data: Dict[str, Any], items: List[Dict[str, Any]], db_name: str = "data/orders.db") -> Dict[str, Any]:
    """
    Create a new order and its items in the database.
    Args:
        order_data: Dictionary containing order details
        items: List of dictionaries containing order item details
        db_name: Database file path
    Returns:
        Dictionary containing the created order with items
    """
    with get_db(db_name) as conn:
        cursor = conn.cursor()
        try:
            # Insert order
            cursor.execute("""
                INSERT INTO orders (
                    order_number, status, created_date, total,
                    requester
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                order_data["order_number"],
                order_data["status"],
                datetime.now().isoformat(),
                order_data["total"],
                order_data["requester"]
            ))
            
            order_id = cursor.lastrowid

            # Insert order items
            for item in items:
                item_total = item["qty_ordered"] * item["price"]
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, item_code, item_description,
                        project, qty_ordered, price, total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    item["item_code"],
                    item["item_description"],
                    item["project"],
                    item["qty_ordered"],
                    item["price"],
                    item_total
                ))

            # Fetch the created order with items
            cursor.execute("""
                SELECT 
                    o.*,
                    json_group_array(
                        json_object(
                            'item_code', i.item_code,
                            'item_description', i.item_description,
                            'project', i.project,
                            'qty_ordered', i.qty_ordered,
                            'price', i.price,
                            'total', i.total
                        )
                    ) as items
                FROM orders o
                LEFT JOIN order_items i ON o.id = i.order_id
                WHERE o.id = ?
                GROUP BY o.id
            """, (order_id,))
            
            conn.commit()
            return dict(cursor.fetchone())

        except sqlite3.Error:
            conn.rollback()
            raise

def init_db(db_name: str = "data/orders.db"):
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL CHECK(status IN ('Pending', 'Awaiting Authorisation', 'Authorised', 'Received', 'Deleted')),
            created_date TEXT NOT NULL,
            received_date TEXT,
            total REAL NOT NULL DEFAULT 0.0,
            order_note TEXT,
            supplier_note TEXT,
            requester TEXT
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_code TEXT,
            item_description TEXT,
            project TEXT,
            qty_ordered INTEGER NOT NULL,
            qty_received INTEGER,
            price REAL,
            total REAL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)
    
    # Create attachments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rights TEXT NOT NULL CHECK(rights IN ('View', 'Edit'))
        )
    """)
    
    # Create items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT NOT NULL UNIQUE,
            item_description TEXT
        )
    """)
    
    # Create projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT NOT NULL UNIQUE
        )
    """)
    
    # Create audit_trail table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            action_date TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    """)
    
    # Initialize default settings
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("auth_threshold", "10000"))
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("order_number_start", "PO001"))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
