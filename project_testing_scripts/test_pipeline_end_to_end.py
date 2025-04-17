import requests
import sqlite3
import os
from datetime import datetime


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


def create_order():
   payload = {
       "requester": "PipelineTestUser",
       "supplier_id": 1,
       "order_note": "Pipeline test note",
       "supplier_note": "Deliver ASAP",
       "items": [
           {
               "item_code": "PIPE001",
               "item_description": "Steel Pipe 2-inch",
               "project": "TestProject1",
               "qty_ordered": 4,
               "price": 250.0
           },
           {
               "item_code": "JOINT002",
               "item_description": "Pipe Joint 2-inch",
               "project": "TestProject2",
               "qty_ordered": 10,
               "price": 40.0
           }
       ]
   }


   response = requests.post(f"{BASE_URL}/orders", json=payload)
   assert_condition(response.status_code == 200, "Order creation succeeded")
   return response.json()["order"]["id"], response.json()["order"]["order_number"]


def check_order_in_db(order_id):
   order = fetch_from_db("SELECT requester, order_note, supplier_note, status, total FROM orders WHERE id = ?", (order_id,))
   assert_condition(len(order) == 1, "Order record exists in DB")
   return order[0]


def check_order_items(order_id):
   items = fetch_from_db("SELECT item_code, item_description, qty_ordered FROM order_items WHERE order_id = ?", (order_id,))
   assert_condition(len(items) == 2, "Correct number of order items")
   return items


def receive_order(order_id):
   payload = {
       "order_id": order_id,
       "items": [
           {"item_code": "PIPE001", "qty_received": 4},
           {"item_code": "JOINT002", "qty_received": 10}
       ]
   }
   response = requests.post(f"{BASE_URL}/orders/receive", json=payload)
   assert_condition(response.status_code == 200, "Order receiving succeeded")


def check_audit_trail(order_id):
   trail = fetch_from_db("SELECT action, details FROM audit_trail WHERE order_id = ?", (order_id,))
   assert_condition(len(trail) >= 2, "Audit trail entries exist for received items")


def upload_attachment(order_id):
   test_file_path = "/Users/stevencohen/Desktop/test_invoice.pdf"
   if not os.path.exists(test_file_path):
       with open(test_file_path, "wb") as f:
           f.write(b"Dummy content for pipeline test")


   with open(test_file_path, "rb") as f:
       response = requests.post(
           f"{BASE_URL}/orders/upload_attachment",
           files={"file": f},
           data={"order_id": str(order_id)}
       )
   assert_condition(response.status_code == 200, "Attachment uploaded successfully")


def check_attachment_record(order_id):
   files = fetch_from_db("SELECT filename FROM attachments WHERE order_id = ?", (order_id,))
   assert_condition(len(files) >= 1, "Attachment record found in DB")


def main():
   print("🚀 Running full pipeline integration test...\n")
   order_id, order_number = create_order()
   check_order_in_db(order_id)
   check_order_items(order_id)
   receive_order(order_id)
   check_audit_trail(order_id)
   upload_attachment(order_id)
   check_attachment_record(order_id)
   print(f"\n🎉 Pipeline test passed for order {order_number} (ID: {order_id})")


if __name__ == "__main__":
   main()

