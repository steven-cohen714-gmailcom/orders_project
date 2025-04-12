# Purchase Order System for Universal Recycling


This project is a Purchase Order system built for **Universal Recycling**, a metals recycling company based in South Africa.


The system tracks purchase orders from creation to completion with full audit trails, status management, and integrated features such as file attachments, supplier lookups, and WhatsApp notifications via Twilio.


It uses:
- **FastAPI (Python)** as the backend framework
- **SQLite** for the database
- **HTML + JavaScript** for the frontend (no frameworks)
- **Google Cloud VM** for deployment


---


## 🧰 Development Environment


- **Coding machines**: MacBook Pro or Mac Studio
- **Deployment server**: Google Cloud VM  
  → `ssh steven_cohen714@34.35.73.12`
- **Version control**: GitHub  
  → [GitHub repo](https://github.com/steven-cohen714-gmailcom/orders_project.git)


---


## 📦 Directory Structure


orders_project/
├── backend/
│   ├── endpoints/       # API routes (e.g., /orders, /suppliers)
│   ├── main.py          # FastAPI entry point
│   ├── database.py      # SQLite setup and logic
│   ├── utils/           # Helper functions (dates, file uploads, etc.)
│   ├── models.py        # Optional: database models (e.g., for ORM)
│   └── scrapers/        # Optional: supplier lookup scripts
├── data/
│   ├── attachments/     # Uploaded files (PDFs, Excel, etc.)
│   └── orders.db        # SQLite database
└── frontend/
├── static/
│   ├── css/         # Styling (e.g., styles.css)
│   └── js/          # JavaScript logic (e.g., scripts.js)
└── templates/       # HTML files (e.g., new_order.html, audit.html)


## 🥪 Testing Strategy 
### Unit Tests
- **Located in**: `backend/tests/`
- **Focus**: Individual function validation (e.g., `validate_date`, DB inserts) 
- **Naming**: `test_<module>.py`


 ```python 
def test_validate_date_format():
assert validate_date("11/04/2025") == "11/04/2025" 
with pytest.raises(ValueError): 
validate_date("2025-04-11")


Integration Tests (End-to-End)
Integration tests validate the entire pipeline (e.g., creating an order, updating status, attaching files, sending Twilio notifications). They must:


* Validate 100% of the pipeline
* Include before and after validation for each step
* Provide a validation summary
* Fail with a stacktrace for debugging


Setup:
* Location: backend/tests/integration/
* Dependencies:


pipx runpip fastapi install pytest httpx pytest-asyncio


* Database: Use a test DB (data/test_orders.db)


Example
# backend/tests/integration/test_order_pipeline.py
import pytest
import httpx
import sqlite3
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def setup_test_db():
    print("Before: Setting up test database")
    conn = sqlite3.connect("data/test_orders.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, order_number TEXT, status TEXT)")
    conn.commit()
    yield conn
    print("After: Cleaning up test database")
    conn.close()


@pytest.mark.asyncio
async def test_order_pipeline_end_to_end(client, setup_test_db):
    cursor = setup_test_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    assert cursor.fetchone()[0] == 0, "Database should be empty"


    # Step 1: Create an order
    response = client.post("/orders", json={"order_number": "PO001", "status": "Pending"})
    assert response.status_code == 200, f"Failed to create order: {response.text}"
    order = response.json()
    print("After: Order created -", order)


    # Step 2: Update status
    response = client.put(f"/orders/{order['id']}", json={"status": "Awaiting Authorisation"})
    assert response.status_code == 200, f"Failed to update status: {response.text}"
    updated_order = response.json()
    print("After: Status updated -", updated_order)


    # Step 3: Attach a file (mock)
    response = client.post(f"/orders/{order['id']}/attachments", files={"file": ("test.pdf", b"test content", "application/pdf")})
    assert response.status_code == 200, f"Failed to attach file: {response.text}"
    print("After: File attached")


    # Step 4: Mock Twilio notification
    print("After: Twilio notification sent (mocked)")


    # Validation Summary
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order["id"],))
    final_order = cursor.fetchone()
    print("\nValidation Summary:")
    print(f"- Order exists: {final_order is not None}")
    print(f"- Final status: {final_order[2]} (Expected: Awaiting Authorisation)")
    assert final_order[2] == "Awaiting Authorisation", "Final status mismatch"


Dev Workflow
* Code: On MacBook/Mac Studio using Cursor
* Test: Locally using pytest
* Push: To GitHub:
git add . && git commit -m "Your message" && git push origin main


Deploy: On VM:
ssh steven_cohen714@34.35.73.12
git pull origin main
pipx run --spec fastapi python3 backend/main.py
Best Practices
* Modular Structure: Separate business logic, routes, and utilities
* Docstrings: Comment every function with purpose, inputs, outputs
* Error Handling: Return HTTP status codes with meaningful messages
* PEP8: Use snake_case for functions/vars, PascalCase for classes
* Commits: Consistent messages, e.g., git commit -m "Add order endpoint"
Statuses Tracked
Pending
Awaiting Authorisation (triggered if total > R10,000 — configurable)
Authorised
Received
Deleted (audit trail maintained)


EOF