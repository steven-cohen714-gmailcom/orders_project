import requests
import sqlite3
from datetime import datetime
import os

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

def fetch_all(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def create_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "Partial receive test",
        "note_to_supplier": "Split delivery test",
        "items": [
            {
                "item_code": "PART001",
                "item_description": "Partial Item A",
                "project": "SplitProjA",
                "qty_ordered": 10,
                "price": 100.0
            },
            {
                "item_code": "PART002",
                "item_description": "Partial Item B",
                "project": "SplitProjB",
                "qty_ordered": 5,
                "price": 200.0
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(response.status_code == 200, "Partial order creation succeeded")
    data = response.json()["order"]
    return data["id"], data["order_number"]

def get_item_ids(order_id):
    rows = fetch_all("SELECT id FROM order_items WHERE order_id = ?", (order_id,))
    return [r[0] for r in rows]

def receive_partial(order_id, item_ids):
    payload = [
        {"order_id": order_id, "item_id": item_ids[0], "qty_received": 10},  # full
        {"order_id": order_id, "item_id": item_ids[1], "qty_received": 2},   # partial
    ]
    response = requests.post(f"{BASE_URL}/orders/receive", json=payload)
    print("⚠️ Receive response:", response.status_code, response.text)
    assert_condition(response.status_code == 200, "Partial receipt posted")

def validate_partial(order_id):
    status, received_date = fetch_one("SELECT status, received_date FROM orders WHERE id = ?", (order_id,))
    assert_condition(status == "Pending", "Order status remains Pending")
    assert_condition(received_date is None, "No received_date set for partial receipt")

    row = fetch_one("SELECT qty_received FROM order_items WHERE order_id = ? AND qty_received < qty_ordered", (order_id,))
    assert_condition(row is not None, "At least one item is partially received")

    audit_entries = fetch_all("SELECT action, details FROM audit_trail WHERE order_id = ?", (order_id,))
    assert_condition(len(audit_entries) >= 2, "Audit entries exist for both lines")

def main():
    print("🔍 Running partial receipt test...\n")
    order_id, order_number = create_order()
    item_ids = get_item_ids(order_id)
    receive_partial(order_id, item_ids)
    validate_partial(order_id)
    print(f"\n✅ Partial receipt test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()

