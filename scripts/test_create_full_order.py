import requests

order_payload = {
    "requester": "Aaron",
    "supplier_id": 1,
    "order_note": "Urgent delivery required.",
    "supplier_note": "Please ensure all parts are in stock.",
    "items": [
        {
            "item_code": "VALVE001",
            "item_description": "3-inch BSP Ball Valve",
            "project": "Project X",
            "qty_ordered": 2,
            "price": 1200.50
        },
        {
            "item_code": "FLANGE002",
            "item_description": "Steel Flange 4-hole",
            "project": "Project Y",
            "qty_ordered": 5,
            "price": 350.00
        }
    ]
}

response = requests.post("http://localhost:8004/orders", json=order_payload)
print("Status Code:", response.status_code)
print("Response:", response.json())
