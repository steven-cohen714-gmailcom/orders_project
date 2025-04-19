import requests
import sqlite3
from datetime import datetime

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    print(f"✅ {message}")

def fetch_one(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

def create_high_value_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "Test high value order",
        "note_to_supplier": "Handle with care",
        "items": [
            {
                "item_code": "HIGH001",
                "item_description": "Premium Machine Part",
                "project": "TestProjX",
                "qty_ordered": 1,
                "price": 20000.0  # High price to trigger threshold
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(response.status_code == 200, "Order creation succeeded")
    data = response.json()
    return data["order"]["id"], data["order"]["order_number"]

def check_authorisation_status(order_id):
    row = fetch_one("SELECT status, total FROM orders WHERE id = ?", (order_id,))
    status, total = row
    assert_condition(status == "Awaiting Authorisation", "Status is Awaiting Authorisation")
    assert_condition(total > 10000, "Total is above threshold")

def main():
    print("\n🚨 Running high-value order auth threshold test...\n")
    order_id, order_number = create_high_value_order()
    check_authorisation_status(order_id)
    print(f"\n🎯 Test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()

