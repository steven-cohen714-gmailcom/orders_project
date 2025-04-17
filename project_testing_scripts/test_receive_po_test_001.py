import requests

payload = {
    "order_id": 3,
    "items": [
        { "item_code": "TEST001", "qty_received": 3 },
        { "item_code": "TEST002", "qty_received": 2 }
    ]
}

response = requests.post("http://localhost:8004/orders/receive", json=payload)
print("Status Code:", response.status_code)
print("Response:", response.json())
