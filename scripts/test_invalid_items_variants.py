import requests
import sqlite3
import os

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    print(f"✅ {message}")

def fetch_from_db(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def count_orders():
    return fetch_from_db("SELECT COUNT(*) FROM orders")[0][0]

def send_invalid_payload(payload, expected_error):
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    print(f"⚠️ Full response: {response.status_code} {response.text}")
    assert_condition(response.status_code in (400, 422), "400 or 422 received for invalid payload")
    assert_condition(expected_error.lower() in response.text.lower(), f"Error message contains '{expected_error}'")

def main():
    print("\n🧪 Testing invalid item list edge cases...\n")

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"❌ Cannot find DB at: {DB_PATH}")

    initial_count = count_orders()

    # Case 1: Empty item list
    payload1 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": []
    }
    send_invalid_payload(payload1, "at least one item")

    # Case 2: Missing item_code
    payload2 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": [{
            "item_description": "Missing code",
            "project": "X",
            "qty_ordered": 1,
            "price": 10
        }]
    }
    send_invalid_payload(payload2, "item_code")

    # Case 3: Missing project
    payload3 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": [{
            "item_code": "X123",
            "item_description": "Test",
            "qty_ordered": 1,
            "price": 10
        }]
    }
    send_invalid_payload(payload3, "project")

    final_count = count_orders()
    assert_condition(final_count == initial_count, "❄️ No invalid orders inserted")

    print("\n✅ All item validation tests passed\n")

if __name__ == "__main__":
    main()

