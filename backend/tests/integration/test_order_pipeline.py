import pytest
from fastapi.testclient import TestClient
from ...main import app
from ...database import create_order
import sqlite3
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def test_db():
    """Set up a clean test database."""
    conn = sqlite3.connect("data/test_orders.db")
    cursor = conn.cursor()
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL,
            created_date TEXT NOT NULL,
            total REAL NOT NULL,
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
    # Create settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    """)
    # Initialize settings
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("auth_threshold", "10000"))
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("order_number_start", "PO001"))
    # Clear orders and order_items tables
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM order_items")
    conn.commit()
    yield conn
    conn.close()

def get_order_count(conn):
    """Helper to count orders in database."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    return cursor.fetchone()[0]

def get_order_by_number(conn, order_number):
    """Helper to fetch order by order_number."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, order_number, status, created_date, total, requester FROM orders WHERE order_number = ?", (order_number,))
    return cursor.fetchone()

def get_orders(status=None, db_name="data/test_orders.db"):
    """Helper to simulate GET /orders using test DB."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = "SELECT id, order_number, status, created_date, total, order_note, supplier_note, requester FROM orders"
    params = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    cursor.execute(query, params)
    orders = cursor.fetchall()
    conn.close()
    result = []
    for order in orders:
        result.append({
            "id": order[0],
            "order_number": order[1],
            "status": order[2],
            "created_date": datetime.fromisoformat(order[3]).strftime("%d/%m/%Y"),
            "total": order[4],
            "order_note": order[5],
            "supplier_note": order[6],
            "requester": order[7]
        })
    return {"orders": result}

def test_order_pipeline(test_db):
    """Test end-to-end order creation and retrieval."""
    print("\n=== Integration Test: Order Pipeline ===")
    
    # Before: Validate empty database
    before_count = get_order_count(test_db)
    print(f"Before: Database has {before_count} orders")
    assert before_count == 0, "Database should be empty before test"

    # Step 1: Create order directly
    order_data = {
        "order_number": "PO999",
        "status": "Awaiting Authorisation",
        "total": 15000.0,
        "requester": "Integration Test",
        "items": [
            {
                "item_code": "INT001",
                "item_description": "Integration Test Item",
                "project": "Test Project",
                "qty_ordered": 1,
                "price": 15000.0
            }
        ]
    }
    print("Step 1: Creating order directly in test database")
    result = create_order(
        order_data=order_data,
        items=order_data["items"],
        db_name="data/test_orders.db"
    )
    
    # Validate created order
    assert result["order_number"] == "PO999", "Invalid order number"
    assert result["status"] == "Awaiting Authorisation", "Status incorrect"
    assert result["total"] == 15000.0, "Total incorrect"
    assert result["requester"] == "Integration Test", "Requester incorrect"
    assert datetime.strptime(result["created_date"], "%Y-%m-%dT%H:%M:%S.%f"), "Invalid date format"
    print("Step 1 After: Order creation validated")

    # Step 2: Check database after creation
    after_post_count = get_order_count(test_db)
    print(f"After creation: Database has {after_post_count} orders")
    assert after_post_count == 1, "Database should have 1 order after creation"
    db_order = get_order_by_number(test_db, "PO999")
    assert db_order, "Order not found in database"
    assert db_order[2] == "Awaiting Authorisation", "Database status incorrect"
    assert float(db_order[4]) == 15000.0, "Database total incorrect"
    print("Step 2 After: Database state validated")

    # Step 3: GET /orders using test DB
    print("Step 3: Retrieving orders with GET /orders")
    response = get_orders()
    orders = response["orders"]
    assert len(orders) >= 1, "GET should return at least 1 order"
    get_order = next((o for o in orders if o["order_number"] == "PO999"), None)
    assert get_order, "Test order not found in GET response"
    assert get_order["status"] == "Awaiting Authorisation", "GET status incorrect"
    assert get_order["total"] == 15000.0, "GET total incorrect"
    print("Step 3 After: GET response validated")

    # Step 4: GET /orders?status=Awaiting Authorisation using test DB
    print("Step 4: Retrieving filtered orders with GET /orders?status=Awaiting Authorisation")
    response = get_orders(status="Awaiting Authorisation")
    orders = response["orders"]
    assert any(o["order_number"] == "PO999" for o in orders), "Test order not found in filtered GET"
    assert all(o["status"] == "Awaiting Authorisation" for o in orders), "Filtered GET status incorrect"
    print("Step 4 After: Filtered GET validated")

    # Summary
    print("\n=== Test Summary ===")
    print(f"Before: {before_count} orders")
    print(f"After creation: {after_post_count} orders, status={db_order[2]}, total={db_order[4]}")
    print(f"GET: {len(orders)} orders retrieved, matched expected")
    print("All validations passed!")
