import sqlite3
import logging
from pathlib import Path
import requests

# Setup logging
logging.basicConfig(
    filename="logs/test_preview_order.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def setup_test_data():
    """Insert test data into the database for PDF generation testing."""
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO business_details (id, company_name, address_line1, city, province, postal_code, telephone, vat_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (1, "Test Company", "123 Test St", "Test City", "Test Province", "12345", "123-456-7890", "VAT123"))
        cursor.execute("INSERT OR REPLACE INTO suppliers (id, name) VALUES (?, ?)", (1, "Test Supplier"))
        cursor.execute("INSERT OR REPLACE INTO requesters (id, name) VALUES (?, ?)", (1, "Test Requester"))
        cursor.execute("INSERT OR REPLACE INTO items (item_code, item_description) VALUES (?, ?)", ("ITEM1", "Test Item"))
        cursor.execute("INSERT OR REPLACE INTO projects (project_code, project_name) VALUES (?, ?)", ("PROJ1", "Test Project"))
        cursor.execute("INSERT OR REPLACE INTO settings (id, order_number_start, auth_threshold) VALUES (?, ?, ?)", (1, "URC1000", 1000))
        conn.commit()
        logging.info("Test data inserted successfully")
    except sqlite3.Error as e:
        logging.error(f"Failed to insert test data: {str(e)}", exc_info=True)
        raise
    finally:
        conn.close()

def test_preview_order_endpoint():
    """Test the /orders/pdf/{order_id} endpoint with mock data."""
    try:
        # First, create an order
        payload = {
            "order_number": "URC1000",
            "status": "Pending",
            "total": 20.0,
            "order_note": "",
            "note_to_supplier": "Test note",
            "supplier_id": 1,
            "requester_id": 1,
            "items": [{
                "item_code": "ITEM1",
                "item_description": "Test Item",
                "project": "PROJ1",
                "qty_ordered": 2.0,
                "price": 10.0,
                "total": 20.0
            }]
        }
        response = requests.post("http://localhost:8004/orders", json=payload)
        if response.status_code != 200:
            raise AssertionError(f"Failed to create order: {response.status_code}: {response.text}")

        # Query the database to get the latest order_id
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders WHERE order_number = 'URC1000' ORDER BY id DESC LIMIT 1")
        order_id = cursor.fetchone()[0]
        conn.close()
        if order_id is None:
            raise AssertionError("Failed to retrieve order_id from database")

        # Now test the PDF endpoint with GET
        response = requests.get(f"http://localhost:8004/orders/pdf/{order_id}")
        if response.status_code != 200:
            raise AssertionError(f"Expected status 200, got {response.status_code}: {response.text}")
        if not response.headers.get("content-type", "").startswith("application/pdf"):
            raise AssertionError(f"Expected PDF content-type, got {response.headers.get('content-type')}")
        logging.info("PDF endpoint test passed")
    except Exception as e:
        logging.error(f"PDF endpoint test failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        setup_test_data()
        test_preview_order_endpoint()
        print("All tests passed! Check logs/test_preview_order.log for details.")
    except Exception as e:
        print(f"Test failed: {str(e)}")