# 📦 Orders Project Summary

**Generated:** 2025-04-26 05:19:19

## Overview
The Orders Project is a custom-built Purchase Order system for Universal Recycling Company Pty Ltd, a metals recycling business in South Africa. It allows the company to create, manage, and track purchase orders through various stages: **Pending** → **Awaiting Authorisation** (for orders exceeding the threshold stored in the `settings` table under `auth_threshold`, adjustable in the Maintenance section) → **Authorised** → **Received**. The system includes features like order number generation, Twilio integration for notifications, PDF generation for purchase orders, and a maintenance section for managing company details.

- **User Base**: Less than 10 users, with only 2 having edit rights (others have view-only rights).
- **Deployment**: Hosted on a Google Cloud VM running Debian Linux.
- **Tools**: SQLite, Python, HTML, JavaScript.

## Development Environment
- **Python Version**: 3.13
- **Dependencies** (from `requirements.txt`):
  - fastapi
  - uvicorn
  - jinja2
  - python-multipart
  - twilio
  - python-dotenv

## Current Focus
Today’s tasks include:
- Fixing Twilio/ngrok integration for WhatsApp notifications (triggered when orders exceed the `auth_threshold` value in the `settings` table).
- Resolving order number increment issues (skipping numbers). Note: This may impact PDF generation, as the order number is part of the PDF.
- Updating the New Order screen to display the current order number.
- Implementing PDF generation for the "View Purchase Order" button, with email functionality (depends on fixing order number increment).
- Updating the Maintenance section to include Universal Recycling’s company details.

## 📁 Directory Structure
```
.
├── backend
│   ├── __init__.py
│   ├── __pycache__
│   ├── database.py
│   ├── endpoints
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   ├── html_routes.py
│   │   ├── lookups.py
│   │   ├── orders.py
│   │   ├── requesters.py
│   │   ├── supplier_lookup.py
│   │   └── supplier_lookup_takealot.py
│   ├── main.py
│   ├── scrapers
│   ├── twilio
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── twilio_utils.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       └── order_utils.py
├── data
│   ├── orders.db
│   ├── orders.py
│   ├── printouts
│   │   ├── order_1.txt
│   │   ├── order_3.txt
│   │   └── order_7.txt
│   ├── test_orders.db
│   └── uploads
│       ├── 13_Screenshot_2025-04-23_at_05.19.18.png
│       ├── 14_Screenshot_2025-04-23_at_05.19.18.png
│       ├── 17_Intimisso.pdf
│       ├── 18_Hydehurst RC- Proof of submission.pdf
│       ├── 19_Fidessa Consulting.PDF
│       ├── 20_test_invoice.pdf
│       ├── 21_Fidessa Consulting.PDF
│       ├── 21_test_invoice.pdf
│       ├── 22_Hydehurst RC- Proof of submission.pdf
│       ├── 24_Fidessa Consulting.PDF
│       ├── 25_Screenshot 2025-04-20 at 17.12.14.png
│       ├── 26_Intimisso.pdf
│       ├── 27_test_invoice.pdf
│       ├── 28_Deposit - 2.pdf
│       ├── 28_test_invoice.pdf
│       ├── 30_2025-04-22_18-29.pdf
│       ├── 30_2025-04-22_18-44.pdf
│       ├── 30_2025-04-22_18-44_1.pdf
│       ├── 30_Intimisso.pdf
│       ├── 31_Screenshot_2025-04-23_at_05.19.18.png
│       └── test_invoice.pdf
├── frontend
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       ├── audit_trail.js
│   │       ├── components
│   │       ├── new_order.js
│   │       ├── pending_orders.js
│   │       └── received_orders.js
│   └── templates
│       ├── audit_trail.html
│       ├── home.html
│       ├── index.html
│       ├── login.html
│       ├── maintenance.html
│       ├── new_order.html
│       ├── pending_orders.html
│       ├── print_template.html
│       └── received_orders.html
├── logs
│   ├── db_activity_log.txt
│   ├── lookups_log.txt
│   ├── message_sid_mapping.json
│   ├── new_orders_log.txt
│   ├── phone_order_mapping.json
│   ├── server.log
│   ├── supplier_lookup_debug.log
│   ├── takealot_lookup.log
│   ├── testing_log.txt
│   ├── twilio.log
│   └── whatsapp_log.txt
├── requirements.txt
├── scripts
│   ├── __pycache__
│   ├── add_debug_validation_handler.py
│   ├── clear_transactional_data.py
│   ├── dump_project_summary.py
│   ├── git_pull_project.py
│   ├── git_push_project.py
│   ├── init_db_fresh.py
│   ├── inject_filter_route.py
│   ├── insert_get_all_orders.py
│   ├── insert_next_order_number_route.py
│   ├── insert_pending_route.py
│   ├── insert_print_route.py
│   ├── insert_receive_route.py
│   ├── integration_tests.py
│   ├── prepare_lookup_tables.py
│   ├── repair_orders_routes.py
│   ├── reset_and_test.sh
│   ├── seed_static_data.py
│   ├── start_server.py
│   ├── stuff_we_are_working_on_today.py
│   ├── test_authorisation_threshold_trigger.py
│   ├── test_invalid_data_handling.py
│   ├── test_invalid_items_variants.py
│   ├── test_pipeline_end_to_end.py
│   └── test_receive_partial.py
├── stuff_we_are_working_on_today.md
└── venv
    ├── bin
    │   ├── Activate.ps1
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── dotenv
    │   ├── fastapi
    │   ├── normalizer
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.13
    │   ├── python -> python3.13
    │   ├── python3 -> python3.13
    │   ├── python3.13 -> /opt/homebrew/opt/python@3.13/bin/python3.13
    │   ├── uvicorn
    │   └── wsdump
    ├── include
    │   └── python3.13
    ├── lib
    │   └── python3.13
    │       └── site-packages
    └── pyvenv.cfg

29 directories, 109 files
```

## 🗄️ Database Schema (`data/orders.db`)

### Table `requesters`
- `id` (INTEGER), pk=True, nullable
- `name` (TEXT), pk=False, nullable

### Table `sqlite_sequence`
- `name` (), pk=False, nullable
- `seq` (), pk=False, nullable

### Table `suppliers`
- `id` (INTEGER), pk=True, nullable
- `account_number` (TEXT), pk=False, nullable
- `name` (TEXT), pk=False, nullable
- `telephone` (TEXT), pk=False, nullable
- `vat_number` (TEXT), pk=False, nullable
- `registration_number` (TEXT), pk=False, nullable
- `email` (TEXT), pk=False, nullable
- `contact_name` (TEXT), pk=False, nullable
- `contact_telephone` (TEXT), pk=False, nullable
- `address_line1` (TEXT), pk=False, nullable
- `address_line2` (TEXT), pk=False, nullable
- `address_line3` (TEXT), pk=False, nullable
- `postal_code` (TEXT), pk=False, nullable

### Table `orders`
- `id` (INTEGER), pk=True, nullable
- `order_number` (TEXT), pk=False, nullable
- `status` (TEXT), pk=False, nullable
- `created_date` (TEXT), pk=False, nullable default CURRENT_TIMESTAMP
- `received_date` (TEXT), pk=False, nullable
- `total` (REAL), pk=False, nullable
- `order_note` (TEXT), pk=False, nullable
- `note_to_supplier` (TEXT), pk=False, nullable
- `supplier_id` (INTEGER), pk=False, nullable
- `requester_id` (INTEGER), pk=False, nullable

### Table `order_items`
- `id` (INTEGER), pk=True, nullable
- `order_id` (INTEGER), pk=False, nullable
- `item_code` (TEXT), pk=False, nullable
- `item_description` (TEXT), pk=False, nullable
- `project` (TEXT), pk=False, nullable
- `qty_ordered` (REAL), pk=False, nullable
- `qty_received` (REAL), pk=False, nullable
- `received_date` (TEXT), pk=False, nullable
- `price` (REAL), pk=False, nullable
- `total` (REAL), pk=False, nullable

### Table `attachments`
- `id` (INTEGER), pk=True, nullable
- `order_id` (INTEGER), pk=False, nullable
- `filename` (TEXT), pk=False, not null
- `file_path` (TEXT), pk=False, not null
- `upload_date` (TEXT), pk=False, not null

### Table `audit_trail`
- `id` (INTEGER), pk=True, nullable
- `order_id` (INTEGER), pk=False, nullable
- `action` (TEXT), pk=False, nullable
- `details` (TEXT), pk=False, nullable
- `action_date` (TEXT), pk=False, nullable default CURRENT_TIMESTAMP
- `user_id` (INTEGER), pk=False, nullable

### Table `settings`
- `key` (TEXT), pk=True, nullable
- `value` (TEXT), pk=False, nullable

### Table `users`
- `id` (INTEGER), pk=True, nullable
- `username` (TEXT), pk=False, nullable
- `password_hash` (TEXT), pk=False, not null
- `rights` (TEXT), pk=False, not null

### Table `projects`
- `id` (INTEGER), pk=True, nullable
- `project_code` (TEXT), pk=False, nullable
- `project_name` (TEXT), pk=False, nullable

### Table `items`
- `id` (INTEGER), pk=True, nullable
- `item_code` (TEXT), pk=False, nullable
- `item_description` (TEXT), pk=False, nullable

## 🌍 Environment Variables (`.env`)
Note: Sensitive values like Twilio SSID, auth token, and ngrok token should be stored here.
```plaintext
TWILIO_ACCOUNT_SID=AC78528274fa496d1971ff628cadc23a
TWILIO_AUTH_TOKEN=a30638234faac92dd326e749c67d5070
TWILIO_PHONE_NUMBER=whatsapp:+19472224054
GROUP_MEMBER_1=whatsapp:+27648475358
GROUP_MEMBER_2=
GROUP_MEMBER_3=
GROUP_MEMBER_4=
GROUP_MEMBER_5=
GROUP_MEMBER_6=
GROUP_MEMBER_7=
NGROK_TOKEN=2wFRynZ4XvFxSsrrAMWDWeUQbd2_5NuF5uaXUD5DyLgVjW32M
FLASK_APP=main.py
FLASK_ENV=development```

## 📋 General Requirements

- **Date Format**: All dates must default to today’s date, use the `dd/mm/yyyy` format (allowing `d/m/yyyy` input), and include a calendar component for selection. If possible, support navigation between date sections (day/month/year) using right/left arrow keys.

## 📝 General Notes

- **Server URL**: The application runs on `http://localhost:8004` by default (verified in `main.py`).
- **ngrok Setup**: ngrok should be running to expose the local server for Twilio webhooks. Use the provided ngrok token and username to set up. Current ngrok URL: [To be updated after setup].
- **Twilio Webhook**: Ensure the Twilio webhook for WhatsApp is configured to point to the ngrok URL at `/orders/whatsapp/webhook`.

## 📂 Relevant Files for Current Tasks
### Main Application Setup (`backend/main.py`)

```python
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.endpoints import orders, auth, lookups, html_routes, supplier_lookup, supplier_lookup_takealot
from backend.database import init_db
from pathlib import Path
import logging

# Install debug validator
from scripts.add_debug_validation_handler import install_validation_handler

# Logging setup
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/server_startup.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Initialize DB
try:
    init_db()
    logging.info("✅ Database initialized successfully.")
except Exception as e:
    logging.exception("❌ Failed to initialize database")
    raise

# FastAPI app
app = FastAPI(
    title="Universal Recycling Purchase Order System",
    description="Purchase Order management system for Universal Recycling"
)

# Enhanced validation
install_validation_handler(app)

# Mount folders
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/data/uploads", StaticFiles(directory="data/uploads"), name="uploads")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Routers
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(lookups.router)
app.include_router(html_routes.router)
app.include_router(supplier_lookup.router)
app.include_router(supplier_lookup_takealot.router)

# HTML routes using Jinja2 templates
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/orders/received_orders", response_class=HTMLResponse)
async def received_orders_page(request: Request):
    return templates.TemplateResponse("received_orders.html", {"request": request})

@app.get("/orders/audit_trail", response_class=HTMLResponse)
async def audit_trail_page(request: Request):
    return templates.TemplateResponse("audit_trail.html", {"request": request})

@app.get("/maintenance", response_class=HTMLResponse)
async def maintenance_page(request: Request):
    return templates.TemplateResponse("maintenance.html", {"request": request})

# Run server
if __name__ == "__main__":
    import uvicorn
    try:
        logging.info("🚀 Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8004)
    except Exception as e:
        logging.exception("❌ Server failed to start")
        raise

```
### Twilio Integration (`backend/twilio/twilio_utils.py`)

**Twilio Configuration**:
- **Universal Recycling WhatsApp Number**: +27 64 847-5358 (South Africa)
- **Twilio Number**: +1 947 222 4054
- **Twilio SSID**: AC78528274fa496d197171ff628cadc23a (Note: Store securely in `.env`)
- **Twilio Auth Token**: a30638234faac92dd326e749c67d5070 (Note: Store securely in `.env`)

**ngrok Configuration**:
- **ngrok Username**: tintin@urc.co.za
- **ngrok Token**: 2wFRynZ4XvFxSsrrAMWDWeUQbd2_5NuF5uaXUD5DyLgVjW32M (Note: Store securely in `.env`)

```python
import os
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path
import logging
import json

# Set up logging
logging.basicConfig(
    filename="logs/twilio.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
group_members = [
    os.getenv("GROUP_MEMBER_1"),
    os.getenv("GROUP_MEMBER_2"),
    os.getenv("GROUP_MEMBER_3"),
    os.getenv("GROUP_MEMBER_4"),
    os.getenv("GROUP_MEMBER_5"),
    os.getenv("GROUP_MEMBER_6"),
    os.getenv("GROUP_MEMBER_7"),
]

# Initialize Twilio client
client = Client(account_sid, auth_token)

# File to store phone number to most recent order number mapping
PHONE_ORDER_MAPPING_FILE = Path("logs/phone_order_mapping.json")

def save_phone_order_mapping(phone_number: str, order_number: str):
    mapping = {}
    if PHONE_ORDER_MAPPING_FILE.exists():
        with PHONE_ORDER_MAPPING_FILE.open("r", encoding="utf-8") as f:
            mapping = json.load(f)
    mapping[phone_number] = order_number
    with PHONE_ORDER_MAPPING_FILE.open("w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)

def get_order_number_from_phone(phone_number: str) -> str:
    if not PHONE_ORDER_MAPPING_FILE.exists():
        return None
    with PHONE_ORDER_MAPPING_FILE.open("r", encoding="utf-8") as f:
        mapping = json.load(f)
    return mapping.get(phone_number)

def send_whatsapp_notification(order_number: str, total: float):
    message_body = f"New order {order_number} exceeds threshold (R{total:.2f}). Reply 'Authorised' to approve."
    try:
        for member in group_members:
            if member:  # Skip if member is None (not set in .env)
                message = client.messages.create(
                    body=message_body,
                    from_=twilio_number,
                    to=member
                )
                logging.info(f"Sent WhatsApp message to {member} for order {order_number}: {message.sid}")
                # Save the phone number to order number mapping
                save_phone_order_mapping(member, order_number)
        return True
    except Exception as e:
        logging.error(f"Failed to send WhatsApp notification for order {order_number}: {str(e)}")
        return False
```
### Order Number Generation (`backend/endpoints/orders.py`)

```python
from fastapi import APIRouter, HTTPException, Request, UploadFile, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import json
import shutil

from ..database import create_order, get_setting, update_setting
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items
from backend.twilio.twilio_utils import send_whatsapp_notification, get_order_number_from_phone

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="frontend/templates")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.get("/next_order_number")
def get_next_order_number():
    try:
        current_number = get_setting("order_number_start")
        next_number = generate_order_number(current_number)
        return {"next_order_number": next_number}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "next_order_number"})
        raise HTTPException(status_code=500, detail=f"Failed to get next order number: {e}")

class OrderItem(BaseModel):
    item_code: str = Field(min_length=1)
    item_description: str = Field(min_length=1)
    project: str = Field(min_length=1)
    qty_ordered: float = Field(gt=0)
    price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.qty_ordered * self.price

class OrderCreate(BaseModel):
    order_number: Optional[str] = None
    requester_id: int = Field(gt=0)
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = Field(None, max_length=1000)
    supplier_id: Optional[int] = None
    items: List[OrderItem] = Field(min_length=1)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

@router.post("")
async def create_new_order(order: OrderCreate):
    try:
        validate_order_items(order.items)
        total = order.total

        auth_threshold = float(get_setting("auth_threshold"))
        current_order_number = get_setting("order_number_start")

        if not order.order_number:
            order.order_number = generate_order_number(current_order_number)
            next_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_number)

        status = determine_status(total, auth_threshold)

        if total > auth_threshold:
            send_whatsapp_notification(order.order_number, total)

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Invalid requester_id")

        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        log_event("new_orders_log.txt", {"action": "submit_attempt", "order_data": order_data})

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            name_row = cursor.fetchone()
            result["requester"] = name_row[0] if name_row else "Unknown"

        log_event("new_orders_log.txt", {"action": "submit_success", "order_number": order.order_number, "status": status})

        return {"message": "Order created successfully", "order": result}
    except sqlite3.Error as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "value"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "unexpected"})
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    try:
        # Parse the incoming WhatsApp message
        form_data = await request.form()
        message_body = form_data.get("Body", "").strip().lower()
        from_number = form_data.get("From", "")

        # Log the incoming message
        log_event("whatsapp_log.txt", {
            "action": "received_message",
            "from": from_number,
            "message": message_body
        })

        # Check if the response is "authorised"
        if message_body != "authorised":
            return {"status": "ignored", "message": "Response must be 'Authorised'"}

        # Get the order number from the phone number
        order_number = get_order_number_from_phone(from_number)
        if not order_number:
            log_event("whatsapp_log.txt", {"error": f"No order found for phone number {from_number}"})
            return {"status": "error", "message": "Order not found for this phone number"}

        # Find the order in the database
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, status FROM orders WHERE order_number = ?", (order_number,))
            order = cursor.fetchone()
            if not order:
                log_event("whatsapp_log.txt", {"error": f"Order {order_number} not found"})
                return {"status": "error", "message": "Order not found"}

            order_id, current_status = order
            if current_status != "Awaiting Authorisation":
                log_event("whatsapp_log.txt", {"error": f"Order {order_number} status is {current_status}, cannot authorise"})
                return {"status": "error", "message": "Order not awaiting authorisation"}

            # Update the order status to "Authorised"
            cursor.execute("""
                UPDATE orders
                SET status = 'Authorised'
                WHERE id = ?
            """, (order_id,))
            conn.commit()

            # Log the authorisation in the audit trail
            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Authorised', ?, ?, ?)
            """, (order_id, f"Order authorised via WhatsApp by {from_number}", datetime.now().isoformat(), 0))
            conn.commit()

        log_event("whatsapp_log.txt", {"action": "order_authorised", "order_number": order_number, "from": from_number})
        return {"status": "success", "message": "Order authorised"}
    except Exception as e:
        log_event("whatsapp_log.txt", {"error": str(e), "type": "webhook"})
        return {"status": "error", "message": str(e)}

class ItemReceive(BaseModel):
    order_id: int
    item_id: int
    qty_received: float = Field(gt=0)

@router.post("/receive")
def mark_order_received(receive_data: List[ItemReceive]):
    try:
        now = datetime.now().isoformat()
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            order_ids_updated = set()

            for item in receive_data:
                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ? AND order_id = ?
                """, (item.qty_received, now, item.item_id, item.order_id))

                cursor.execute("""
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, 'Received', ?, ?, ?)
                """, (
                    item.order_id,
                    f"Item ID {item.item_id} received: {item.qty_received}",
                    now,
                    0
                ))

                order_ids_updated.add(item.order_id)

            for order_id in order_ids_updated:
                cursor.execute("""
                    SELECT COUNT(*) FROM order_items
                    WHERE order_id = ? AND (qty_received IS NULL OR qty_received < qty_ordered)
                """, (order_id,))
                incomplete = cursor.fetchone()[0]
                if incomplete == 0:
                    cursor.execute("""
                        UPDATE orders SET status = 'Received', received_date = ?
                        WHERE id = ?
                    """, (now, order_id))

        log_event("new_orders_log.txt", {"action": "receive", "orders": list(order_ids_updated)})
        return {"status": "✅ Order(s) marked as received"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "receive"})
        raise HTTPException(status_code=500, detail=f"Failed to receive order(s): {e}")

@router.post("/upload_attachment")
async def upload_attachment(file: UploadFile, order_id: int = Form(...)):
    try:
        # Validate order_id exists
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Invalid order_id")

        # Sanitize filename and handle duplicates
        filename = file.filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
        base_filename = filename
        saved_path = UPLOAD_DIR / f"{order_id}_{filename}"
        counter = 1
        while saved_path.exists():
            name, ext = base_filename.rsplit(".", 1) if "." in base_filename else (base_filename, "")
            filename = f"{name}_{counter}.{ext}" if ext else f"{name}_{counter}"
            saved_path = UPLOAD_DIR / f"{order_id}_{filename}"
            counter += 1

        # Check file size before saving
        content = await file.read()
        file_size = len(content)
        if file_size < 500:
            raise HTTPException(status_code=400, detail="Uploaded file is too small or corrupt.")

        # Save the file
        with saved_path.open("wb") as buffer:
            buffer.write(content)

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, filename, str(saved_path), datetime.now().isoformat()))
            conn.commit()

        log_event("new_orders_log.txt", {
            "action": "attachment_uploaded",
            "order_id": order_id,
            "filename": filename,
            "path": str(saved_path),
            "size_bytes": file_size
        })

        return {"status": "✅ Attachment uploaded"}
    except sqlite3.Error as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_upload"})
        raise HTTPException(status_code=500, detail=f"Database error during upload: {str(e)}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "upload"})
        raise HTTPException(status_code=500, detail=f"Failed to upload attachment: {str(e)}")
    finally:
        await file.close()

@router.get("/attachments/{order_id}")
def get_order_attachments(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, filename, file_path, upload_date
                FROM attachments
                WHERE order_id = ?
            """, (order_id,))
            files = [dict(row) for row in cursor.fetchall()]
        return {"attachments": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve attachments: {e}")

@router.post("/save_note/{order_id}")
async def save_order_note(order_id: int, data: dict):
    try:
        order_note = data.get("order_note")
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders
                SET order_note = ?
                WHERE id = ?
            """, (order_note, order_id))
            conn.commit()

            cursor.execute("""
                INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                VALUES (?, 'Note Updated', ?, ?, ?)
            """, (order_id, f"Order note updated to: {order_note}", datetime.now().isoformat(), 0))

        log_event("new_orders_log.txt", {"action": "note_updated", "order_id": order_id, "order_note": order_note})
        return {"status": "✅ Order note updated"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "save_note"})
        raise HTTPException(status_code=500, detail=f"Failed to save order note: {e}")

@router.get("/api/orders/pending_orders")
def get_pending_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = []
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        # Include orders that are Pending, Waiting for Approval, Awaiting Authorisation, or Authorised
        filters.append("o.status IN ('Pending', 'Waiting for Approval', 'Awaiting Authorisation', 'Authorised')")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        if status and status != "All":
            filters.append("o.status = ?")
            params.append(status)

        where_clause = " AND ".join(filters)

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                orders.append(order)
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": where_clause, "params": params})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "pending_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load pending orders: {e}")

@router.get("/api/received_orders")
def get_received_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None)
):
    try:
        filters = ["o.status = 'Received'"]
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        where_clause = " AND ".join(filters)

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                orders.append(order)
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": where_clause, "params": params})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "received_orders"})
        raise HTTPException(status_code=500, detail=f"Failed to load received orders: {e}")

@router.get("/api/items_for_order/{order_id}")
def get_items_for_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date, price,
                       (qty_ordered * price) AS total
                FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {e}")

@router.get("/api/audit_trail")
def get_audit_trail(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        filters = []
        params = []

        def validate_date(date_str):
            if not date_str:
                return None
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use yyyy-mm-dd.")

        if start_date:
            start_date = validate_date(start_date)
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
            end_date = validate_date(end_date)
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(end_date)

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        if status and status != "All":
            filters.append("o.status = ?")
            params.append(status)

        where_clause = " AND ".join(filters) if filters else "1=1"

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.received_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.order_note, o.note_to_supplier, o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)
            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
                if order["received_date"]:
                    order["received_date"] = datetime.fromisoformat(order["received_date"]).strftime("%d/%m/%Y")
                # Fetch items for this order
                cursor.execute("""
                    SELECT id, item_code, item_description, project, qty_ordered, qty_received, received_date
                    FROM order_items
                    WHERE order_id = ?
                """, (order["id"],))
                items = [dict(item_row) for item_row in cursor.fetchall()]
                for item in items:
                    if item["received_date"]:
                        item["received_date"] = datetime.fromisoformat(item["received_date"]).strftime("%d/%m/%Y")
                order["items"] = items
                orders.append(order)
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": where_clause, "params": params})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail: {e}")
```
### New Order Screen (`frontend/templates/new_order.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create New Order</title>
    <link rel="icon" href="data:,">
    <style>
        body { font-family: Arial, sans-serif; padding: 2rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
        .status { font-weight: bold; }
        .filters { margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
        .filters label { font-weight: bold; }
        input[type="date"], select, textarea, input[type="number"], input[type="text"] {
            padding: 0.4rem;
            font-size: 1rem;
            font-family: monospace;
        }
        button {
            padding: 0.5rem 1rem;
            cursor: pointer;
            margin-top: 1rem;
            margin-right: 1rem;
        }
        label {
            display: block;
            font-weight: bold;
            margin-top: 1rem;
        }
    </style>
</head>
<body>

    <div>
        <h2>Create Purchase Order</h2>
        <div>
            <div>
                <label for="requester_id">Requester *</label>
                <select id="requester_id" name="requester_id">
                    <option value="">Select Requester</option>
                    {% for requester in requesters %}
                    <option value="{{ requester.id }}">{{ requester.name }}</option>
                    {% endfor %}
                </select>
                <label for="supplier_id">Supplier *</label>
                <select id="supplier_id" name="supplier_id">
                    <option value="">Select Supplier</option>
                    {% for supplier in suppliers %}
                    <option value="{{ supplier.id }}">{{ supplier.name }}</option>
                    {% endfor %}
                </select>
                <label for="note_to_supplier">Note to Supplier</label>
                <textarea id="note_to_supplier" name="note_to_supplier" rows="3"></textarea>
            </div>
            <div>
                <label>Delivery Address</label>
                <div>
                    Universal Recycling Company Pty Ltd<br>
                    [Address Line 1 from DB]<br>
                    [Address Line 2 from DB]<br>
                    [City, Province, Area Code from DB]<br>
                    Telephone: [Telephone from DB]<br>
                    VAT Number: [VAT Number from DB]
                </div>
            </div>
        </div>

        <table id="items-table">
            <thead>
                <tr>
                    <th>Item Code</th>
                    <th>Description</th>
                    <th>Project</th>
                    <th>Qty Ordered</th>
                    <th>Price (R)</th>
                    <th>Total (R)</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <select name="items[0][item_code]" id="item_code_0" onchange="updateItemDescription(0)">
                            <option value="">Select Item</option>
                            {% for item in items %}
                            <option value="{{ item.item_code }}" data-description="{{ item.item_description }}">{{ item.item_code }}</option>
                            {% endfor %}
                        </select>
                    </td>
                    <td><input type="text" name="items[0][item_description]" id="item_description_0" readonly></td>
                    <td>
                        <select name="items[0][project]" id="project_0">
                            <option value="">Select Project</option>
                            {% for project in projects %}
                            <option value="{{ project.project_code }}">{{ project.project_code }}</option>
                            {% endfor %}
                        </select>
                    </td>
                    <td><input type="number" name="items[0][qty_ordered]" id="qty_ordered_0" step="1" min="1" value="1" onchange="updateTotal(0)"></td>
                    <td><input type="number" name="items[0][price]" id="price_0" step="0.01" min="0" value="0" onchange="updateTotal(0)"></td>
                    <td><input type="text" name="items[0][total]" id="total_0" readonly></td>
                    <td><button type="button" onclick="removeRow(this)">Remove</button></td>
                </tr>
            </tbody>
        </table>
        <button type="button" onclick="addRow()">Add Item</button>

        <div>
            <label>Total: R <span id="grand-total">0.00</span></label>
            <div>Excluding VAT</div>
        </div>

        <div>
            <button type="button" id="view-po" onclick="viewPurchaseOrder()">View Purchase Order</button>
            <button type="button" id="email-po" onclick="emailPurchaseOrder()">Email Purchase Order</button>
            <button type="submit" onclick="submitForm()">Submit Order</button>
            <button type="button" onclick="cancelForm()">Cancel</button>
        </div>
    </div>

    <script>
        console.log("Requesters data:", {{ requesters | tojson }});
        console.log("Suppliers data:", {{ suppliers | tojson }});

        let rowCount = 1;

        window.addEventListener('load', function() {
            console.log("Page loaded");
            console.log("Requester dropdown options:", document.getElementById('requester_id').options.length);
            console.log("Supplier dropdown options:", document.getElementById('supplier_id').options.length);
        });

        function addRow() {
            console.log("Adding new row, rowCount:", rowCount);
            const tbody = document.querySelector("#items-table tbody");
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>
                    <select name="items[${rowCount}][item_code]" id="item_code_${rowCount}" onchange="updateItemDescription(${rowCount})">
                        <option value="">Select Item</option>
                        {% for item in items %}
                        <option value="{{ item.item_code }}" data-description="{{ item.item_description }}">{{ item.item_code }}</option>
                        {% endfor %}
                    </select>
                </td>
                <td><input type="text" name="items[${rowCount}][item_description]" id="item_description_${rowCount}" readonly></td>
                <td>
                    <select name="items[${rowCount}][project]" id="project_${rowCount}">
                        <option value="">Select Project</option>
                        {% for project in projects %}
                        <option value="{{ project.project_code }}">{{ project.project_code }}</option>
                        {% endfor %}
                    </select>
                </td>
                <td><input type="number" name="items[${rowCount}][qty_ordered]" id="qty_ordered_${rowCount}" step="1" min="1" value="1" onchange="updateTotal(${rowCount})"></td>
                <td><input type="number" name="items[${rowCount}][price]" id="price_${rowCount}" step="0.01" min="0" value="0" onchange="updateTotal(${rowCount})"></td>
                <td><input type="text" name="items[${rowCount}][total]" id="total_${rowCount}" readonly></td>
                <td><button type="button" onclick="removeRow(this)">Remove</button></td>
            `;
            tbody.appendChild(row);
            rowCount++;
            updateGrandTotal();
        }

        function removeRow(button) {
            if (rowCount > 1) {
                console.log("Removing row, rowCount before:", rowCount);
                button.parentElement.parentElement.remove();
                rowCount--;
                console.log("Row removed, rowCount after:", rowCount);
                updateGrandTotal();
            }
        }

        function updateItemDescription(index) {
            console.log("Updating item description for index:", index);
            const select = document.getElementById(`item_code_${index}`);
            const descriptionInput = document.getElementById(`item_description_${index}`);
            const selectedOption = select.options[select.selectedIndex];
            descriptionInput.value = selectedOption.getAttribute("data-description") || "";
            updateTotal(index);
        }

        function updateTotal(index) {
            console.log("Updating total for index:", index);
            const qty = parseFloat(document.getElementById(`qty_ordered_${index}`).value) || 0;
            const price = parseFloat(document.getElementById(`price_${index}`).value) || 0;
            const total = qty * price;
            document.getElementById(`total_${index}`).value = total.toFixed(2);
            updateGrandTotal();
        }

        function updateGrandTotal() {
            console.log("Updating grand total");
            let grandTotal = 0;
            for (let i = 0; i < rowCount; i++) {
                const totalField = document.getElementById(`total_${i}`);
                if (totalField) {
                    grandTotal += parseFloat(totalField.value) || 0;
                }
            }
            document.getElementById("grand-total").textContent = grandTotal.toFixed(2);
        }

        async function submitForm() {
            console.log("submitForm started");

            const supplierId = document.getElementById("supplier_id").value;
            console.log("Supplier ID:", supplierId);
            const requesterId = document.getElementById("requester_id").value;
            console.log("Requester ID:", requesterId);
            const noteToSupplier = document.getElementById("note_to_supplier").value;
            console.log("Note to Supplier:", noteToSupplier);

            const items = [];
            for (let i = 0; i < rowCount; i++) {
                const itemCode = document.getElementById(`item_code_${i}`)?.value;
                const itemDescription = document.getElementById(`item_description_${i}`)?.value;
                const project = document.getElementById(`project_${i}`)?.value;
                const qtyOrdered = document.getElementById(`qty_ordered_${i}`)?.value;
                const price = document.getElementById(`price_${i}`)?.value;
                if (itemCode && itemDescription && project && qtyOrdered && price) {
                    const item = {
                        item_code: itemCode,
                        item_description: itemDescription,
                        project: project,
                        qty_ordered: parseFloat(qtyOrdered),
                        price: parseFloat(price)
                    };
                    items.push(item);
                }
            }
            console.log("Items collected:", items);

            // Validation
            if (!supplierId) {
                console.log("Validation failed: No supplier selected");
                alert("Please select a supplier.");
                return;
            }
            if (!requesterId) {
                console.log("Validation failed: No requester selected");
                alert("Please select a requester.");
                return;
            }
            if (items.length === 0) {
                console.log("Validation failed: No items added");
                alert("Please add at least one item with all required fields.");
                return;
            }

            // Create JSON payload
            const payload = {
                supplier_id: parseInt(supplierId),
                requester_id: parseInt(requesterId),
                note_to_supplier: noteToSupplier,
                items: items
            };
            console.log("Submitting order with JSON data:", payload);

            // Send JSON request
            try {
                const response = await fetch("/orders", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });
                console.log("Response received, status:", response.status);

                const result = await response.json();
                console.log("Response JSON:", result);

                if (response.ok) {
                    console.log("Order created successfully");
                    alert(`Order created successfully: ${result.order.order_number}`);
                    window.location.href = "/orders/pending_orders"; // Updated URL
                } else {
                    console.log("Failed to create order, details:", result.detail);
                    alert("Failed to create order: " + (typeof result.detail === 'string' ? result.detail : JSON.stringify(result.detail)));
                }
            } catch (error) {
                console.error("Error during fetch:", error);
                alert("An error occurred while submitting the order: " + error.message);
            }
        }

        function emailPurchaseOrder() {
            console.log("Email Purchase Order clicked");
            alert("Email Purchase Order functionality will be implemented after fixing PDF generation.");
        }

        function viewPurchaseOrder() {
            console.log("View Purchase Order clicked");
            alert("View Purchase Order functionality will be implemented after fixing PDF generation.");
            window.location.href = "/orders/pending_orders"; // Updated URL
        }

        function cancelForm() {
            console.log("Cancel button clicked");
            window.location.href = "/orders/pending_orders"; // Updated URL
        }

        window.addRow = addRow;
        window.removeRow = removeRow;
        window.updateItemDescription = updateItemDescription;
        window.updateTotal = updateTotal;
        window.submitForm = submitForm;
        window.emailPurchaseOrder = emailPurchaseOrder;
        window.viewPurchaseOrder = viewPurchaseOrder;
        window.cancelForm = cancelForm;
    </script>
</body>
</html>
```
### Note: PDF Generation Logic

The `View Purchase Order` button logic is in `frontend/templates/new_order.html` (above) and the `/orders` endpoint in `backend/endpoints/orders.py` (above).
### Maintenance Section (`frontend/templates/maintenance.html`)

**Company Details Format**:
```
Delivery Address
Universal Recycling Company Pty Ltd
[Address Line 1 from DB]
[Address Line 2 from DB]
[City, Province, Area Code from DB]
Telephone: [Telephone from DB]
VAT Number: [VAT Number from DB]
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Maintenance - Universal Recycling</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 2rem; }
    .tabs { display: flex; gap: 1rem; margin-bottom: 1rem; }
    .tab { padding: 0.5rem 1rem; cursor: pointer; background: #ddd; border-radius: 4px 4px 0 0; }
    .tab.active { background: #007BFF; color: white; }
    .tab-content { display: none; padding: 1rem; border: 1px solid #ccc; border-radius: 0 4px 4px 4px; }
    .tab-content.active { display: block; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
    input, select, button { padding: 0.4rem; margin: 0.2rem 0; }
    button { cursor: pointer; background: #007BFF; color: white; border: none; border-radius: 4px; }
    button:hover { background: #0056b3; }
    .form-group { margin-bottom: 1rem; }
    .form-group label { display: block; font-weight: bold; }
  </style>
</head>
<body>
  <h2>Maintenance</h2>

  <div class="tabs">
    <div class="tab active" data-tab="users">Users</div>
    <div class="tab" data-tab="requesters">Requesters</div>
    <div class="tab" data-tab="items">Items</div>
    <div class="tab" data-tab="projects">Projects</div>
    <div class="tab" data-tab="settings">Settings</div>
  </div>

  <div id="users" class="tab-content active">
    <form class="form-group" onsubmit="event.preventDefault(); addUser();">
      <label for="user-username">Username:</label>
      <input type="text" id="user-username" autocomplete="username" />
      <label for="user-password">Password:</label>
      <input type="password" id="user-password" autocomplete="current-password" />
      <label for="user-rights">Rights:</label>
      <select id="user-rights">
        <option value="edit">Edit</option>
        <option value="view">View Only</option>
        <option value="admin">Admin</option>
      </select>
      <button type="submit">Add User</button>
    </form>
    <table id="users-table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Rights</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div id="requesters" class="tab-content">
    <div class="form-group">
      <label for="requester-name">Name:</label>
      <input type="text" id="requester-name" />
      <button onclick="addRequester()">Add Requester</button>
    </div>
    <table id="requesters-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div id="items" class="tab-content">
    <div class="form-group">
      <label for="item-code">Item Code:</label>
      <input type="text" id="item-code" />
      <label for="item-description">Description:</label>
      <input type="text" id="item-description" />
      <button onclick="addItem()">Add Item</button>
    </div>
    <table id="items-table">
      <thead>
        <tr>
          <th>Item Code</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div id="projects" class="tab-content">
    <div class="form-group">
      <label for="project-code">Project Code:</label>
      <input type="text" id="project-code" />
      <label for="project-name">Project Name:</label>
      <input type="text" id="project-name" />
      <button onclick="addProject()">Add Project</button>
    </div>
    <table id="projects-table">
      <thead>
        <tr>
          <th>Project Code</th>
          <th>Project Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div id="settings" class="tab-content">
    <div class="form-group">
      <label for="order-number-start">Start Order Number:</label>
      <input type="text" id="order-number-start" />
      <label for="auth-threshold">Authorization Threshold (R):</label>
      <input type="number" id="auth-threshold" step="0.01" />
      <button onclick="updateSettings()">Update</button>
    </div>
  </div>

  <script>
    // Tab switching
    document.querySelectorAll(".tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(tab.dataset.tab).classList.add("active");
      });
    });

    // Load data on page load
    async function loadData(endpoint, tableId, renderRow) {
      try {
        const res = await fetch(endpoint);
        const data = await res.json();
        const tbody = document.querySelector(`#${tableId} tbody`);
        tbody.innerHTML = "";
        Object.values(data)[0].forEach(item => {
          const row = document.createElement("tr");
          row.innerHTML = renderRow(item);
          tbody.appendChild(row);
        });
      } catch (err) {
        console.error(`Failed to load ${tableId}:`, err);
      }
    }

    // Users
    async function loadUsers() {
      loadData("/lookups/users", "users-table", user => `
        <td>${user.username}</td>
        <td>${user.rights}</td>
        <td><button onclick="editUser(${user.id}, '${user.username}', '${user.rights}')">Edit</button></td>
      `);
    }

    async function addUser() {
      const username = document.getElementById("user-username").value;
      const password = document.getElementById("user-password").value;
      const rights = document.getElementById("user-rights").value;
      try {
        await fetch("/lookups/users", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password, rights }),
        });
        loadUsers();
      } catch (err) {
        console.error("Failed to add user:", err);
      }
    }

    async function editUser(id, username, rights) {
      const newUsername = prompt("New Username:", username);
      const newRights = prompt("New Rights (edit/view/admin):", rights);
      if (newUsername && newRights) {
        try {
          await fetch(`/lookups/users/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: newUsername, rights: newRights }),
          });
          loadUsers();
        } catch (err) {
          console.error("Failed to edit user:", err);
        }
      }
    }

    // Requesters
    async function loadRequesters() {
      loadData("/lookups/requesters", "requesters-table", requester => `
        <td>${requester.name}</td>
        <td><button onclick="editRequester(${requester.id}, '${requester.name}')">Edit</button></td>
      `);
    }

    async function addRequester() {
      const name = document.getElementById("requester-name").value;
      try {
        await fetch("/lookups/requesters", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name }),
        });
        loadRequesters();
      } catch (err) {
        console.error("Failed to add requester:", err);
      }
    }

    async function editRequester(id, name) {
      const newName = prompt("New Name:", name);
      if (newName) {
        try {
          await fetch(`/lookups/requesters/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newName }),
          });
          loadRequesters();
        } catch (err) {
          console.error("Failed to edit requester:", err);
        }
      }
    }

    // Items
    async function loadItems() {
      loadData("/lookups/items", "items-table", item => `
        <td>${item.item_code}</td>
        <td>${item.item_description}</td>
        <td><button onclick="editItem(${item.id}, '${item.item_code}', '${item.item_description}')">Edit</button></td>
      `);
    }

    async function addItem() {
      const itemCode = document.getElementById("item-code").value;
      const itemDescription = document.getElementById("item-description").value;
      try {
        await fetch("/lookups/items", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ item_code: itemCode, item_description: itemDescription }),
        });
        loadItems();
      } catch (err) {
        console.error("Failed to add item:", err);
      }
    }

    async function editItem(id, itemCode, itemDescription) {
      const newItemCode = prompt("New Item Code:", itemCode);
      const newItemDescription = prompt("New Description:", itemDescription);
      if (newItemCode && newItemDescription) {
        try {
          await fetch(`/lookups/items/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_code: newItemCode, item_description: newItemDescription }),
          });
          loadItems();
        } catch (err) {
          console.error("Failed to edit item:", err);
        }
      }
    }

    // Projects
    async function loadProjects() {
      loadData("/lookups/projects", "projects-table", project => `
        <td>${project.project_code}</td>
        <td>${project.project_name}</td>
        <td><button onclick="editProject(${project.id}, '${project.project_code}', '${project.project_name}')">Edit</button></td>
      `);
    }

    async function addProject() {
      const projectCode = document.getElementById("project-code").value;
      const projectName = document.getElementById("project-name").value;
      try {
        await fetch("/lookups/projects", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ project_code: projectCode, project_name: projectName }),
        });
        loadProjects();
      } catch (err) {
        console.error("Failed to add project:", err);
      }
    }

    async function editProject(id, projectCode, projectName) {
      const newProjectCode = prompt("New Project Code:", projectCode);
      const newProjectName = prompt("New Project Name:", projectName);
      if (newProjectCode && newProjectName) {
        try {
          await fetch(`/lookups/projects/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ project_code: newProjectCode, project_name: newProjectName }),
          });
          loadProjects();
        } catch (err) {
          console.error("Failed to edit project:", err);
        }
      }
    }

    // Settings
    async function loadSettings() {
      try {
        const res = await fetch("/lookups/settings");
        const data = await res.json();
        document.getElementById("order-number-start").value = data.order_number_start || "";
        document.getElementById("auth-threshold").value = data.auth_threshold || "";
      } catch (err) {
        console.error("Failed to load settings:", err);
      }
    }

    async function updateSettings() {
      const orderNumberStart = document.getElementById("order-number-start").value;
      const authThreshold = document.getElementById("auth-threshold").value;
      try {
        await fetch("/lookups/settings", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ key: "order_number_start", value: orderNumberStart }),
        });
        await fetch("/lookups/settings", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ key: "auth_threshold", value: authThreshold }),
        });
        alert("Settings updated successfully");
      } catch (err) {
        console.error("Failed to update settings:", err);
      }
    }

    // Load all data on page load
    document.addEventListener("DOMContentLoaded", () => {
      loadUsers();
      loadRequesters();
      loadItems();
      loadProjects();
      loadSettings();
    });
  </script>
</body>
</html>
```
