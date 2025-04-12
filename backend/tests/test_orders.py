import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..utils.order_utils import generate_order_number, determine_status

client = TestClient(app)

def test_generate_order_number():
    assert generate_order_number("PO001") == "PO002"
    assert generate_order_number("PO999") == "PO1000"

def test_determine_status():
    assert determine_status(5000.0, 10000.0) == "Pending"
    assert determine_status(15000.0, 10000.0) == "Awaiting Authorisation"

def test_create_order():
    test_order = {
        "requester": "Test User",
        "total": 5000.0,
        "items": [
            {
                "item_code": "TEST001",
                "item_description": "Test Item",
                "project": "Test Project",
                "qty_ordered": 1,
                "price": 5000.0
            }
        ]
    }
    
    response = client.post("/orders", json=test_order)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Order created successfully"
    assert data["order"]["status"] == "Pending" 