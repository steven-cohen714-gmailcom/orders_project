import sqlite3
import os

def init_db():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect("data/orders.db")
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
    
    # Create users table (Maintenance: Manage Users)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rights TEXT NOT NULL CHECK(rights IN ('View', 'Edit'))
        )
    """)
    
    # Create items table (Maintenance: Manage Items)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT NOT NULL UNIQUE,
            item_description TEXT
        )
    """)
    
    # Create projects table (Maintenance: Manage Projects)
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
    
    # Create settings table (Maintenance: Order Number Start, Authorization Threshold)
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
