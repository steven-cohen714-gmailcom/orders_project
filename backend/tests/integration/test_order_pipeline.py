import pytest
from fastapi.testclient import TestClient
from ...main import app
import sqlite3

client = TestClient(app)

@pytest.fixture
def test_db():
    conn = sqlite3.connect("data/test_orders.db")
    yield conn
    conn.close()

def test_complete_order_flow(test_db):
    # Create order
    order_data = {
        "requester": "Integration Test",
        "total": 15000.0,
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
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    order = response.json()["order"]
    assert order["status"] == "Awaiting Authorisation" 