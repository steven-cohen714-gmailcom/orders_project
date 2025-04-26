# 📦 Project Snapshot

**Generated:** 2025-04-26 13:51:28


## 📁 Directory Tree
```
.
├── backend
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── database.cpython-313.pyc
│   │   └── main.cpython-313.pyc
│   ├── database.py
│   ├── endpoints
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── auth.cpython-313.pyc
│   │   │   ├── html_routes.cpython-313.pyc
│   │   │   ├── lookups.cpython-313.pyc
│   │   │   ├── orders.cpython-313.pyc
│   │   │   ├── supplier_lookup.cpython-313.pyc
│   │   │   └── supplier_lookup_takealot.cpython-313.pyc
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
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   └── twilio_utils.cpython-313.pyc
│   │   └── twilio_utils.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-313.pyc
│       │   └── order_utils.cpython-313.pyc
│       └── order_utils.py
├── data
│   ├── orders.db
│   ├── orders.py
│   ├── pdfs
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
│       ├── 43_Intimisso.pdf
│       └── test_invoice.pdf
├── frontend
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       ├── audit_trail.js
│   │       ├── components
│   │       │   ├── attachment_modal.js
│   │       │   ├── expand_line_items.js
│   │       │   ├── order_note_modal.js
│   │       │   ├── receive_modal.js
│   │       │   └── shared_filters.js
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
├── project_summary.md
├── requirements.txt
├── scripts
│   ├── __pycache__
│   │   └── add_debug_validation_handler.cpython-313.pyc
│   ├── add_debug_validation_handler.py
│   ├── clear_transactional_data.py
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
│   ├── project_summary.py
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
└── venv
    ├── bin
    │   ├── Activate.ps1
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── chardetect
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
    │           ├── MarkupSafe-3.0.2.dist-info
    │           ├── PIL
    │           ├── PyJWT-2.10.1.dist-info
    │           ├── PySocks-1.7.1.dist-info
    │           ├── __pycache__
    │           ├── aiohappyeyeballs
    │           ├── aiohappyeyeballs-2.6.1.dist-info
    │           ├── aiohttp
    │           ├── aiohttp-3.11.18.dist-info
    │           ├── aiohttp_retry
    │           ├── aiohttp_retry-2.9.1.dist-info
    │           ├── aiosignal
    │           ├── aiosignal-1.3.2.dist-info
    │           ├── annotated_types
    │           ├── annotated_types-0.7.0.dist-info
    │           ├── anyio
    │           ├── anyio-4.9.0.dist-info
    │           ├── attr
    │           ├── attrs
    │           ├── attrs-25.3.0.dist-info
    │           ├── beautifulsoup4-4.13.4.dist-info
    │           ├── bs4
    │           ├── certifi
    │           ├── certifi-2025.1.31.dist-info
    │           ├── chardet
    │           ├── chardet-5.2.0.dist-info
    │           ├── charset_normalizer
    │           ├── charset_normalizer-3.4.1.dist-info
    │           ├── click
    │           ├── click-8.1.8.dist-info
    │           ├── dotenv
    │           ├── fastapi
    │           ├── fastapi-0.115.12.dist-info
    │           ├── frozenlist
    │           ├── frozenlist-1.6.0.dist-info
    │           ├── h11
    │           ├── h11-0.14.0.dist-info
    │           ├── idna
    │           ├── idna-3.10.dist-info
    │           ├── itsdangerous
    │           ├── itsdangerous-2.2.0.dist-info
    │           ├── jinja2
    │           ├── jinja2-3.1.6.dist-info
    │           ├── jwt
    │           ├── markupsafe
    │           ├── multidict
    │           ├── multidict-6.4.3.dist-info
    │           ├── multipart
    │           ├── outcome
    │           ├── outcome-1.3.0.post0.dist-info
    │           ├── pillow-11.2.1.dist-info
    │           ├── pip
    │           ├── pip-25.0.1.dist-info
    │           ├── propcache
    │           ├── propcache-0.3.1.dist-info
    │           ├── pydantic
    │           ├── pydantic-2.11.3.dist-info
    │           ├── pydantic_core
    │           ├── pydantic_core-2.33.1.dist-info
    │           ├── python_dotenv-1.1.0.dist-info
    │           ├── python_multipart
    │           ├── python_multipart-0.0.20.dist-info
    │           ├── reportlab
    │           ├── reportlab-4.4.0.dist-info
    │           ├── requests
    │           ├── requests-2.32.3.dist-info
    │           ├── selenium
    │           ├── selenium-4.31.0.dist-info
    │           ├── sniffio
    │           ├── sniffio-1.3.1.dist-info
    │           ├── socks.py
    │           ├── sockshandler.py
    │           ├── sortedcontainers
    │           ├── sortedcontainers-2.4.0.dist-info
    │           ├── soupsieve
    │           ├── soupsieve-2.6.dist-info
    │           ├── starlette
    │           ├── starlette-0.46.2.dist-info
    │           ├── trio
    │           ├── trio-0.29.0.dist-info
    │           ├── trio_websocket
    │           ├── trio_websocket-0.12.2.dist-info
    │           ├── twilio
    │           ├── twilio-9.5.2.dist-info
    │           ├── typing_extensions-4.13.2.dist-info
    │           ├── typing_extensions.py
    │           ├── typing_inspection
    │           ├── typing_inspection-0.4.0.dist-info
    │           ├── urllib3
    │           ├── urllib3-2.4.0.dist-info
    │           ├── uvicorn
    │           ├── uvicorn-0.34.2.dist-info
    │           ├── websocket
    │           ├── websocket_client-1.8.0.dist-info
    │           ├── wsproto
    │           ├── wsproto-1.2.0.dist-info
    │           ├── yarl
    │           └── yarl-1.20.0.dist-info
    └── pyvenv.cfg

125 directories, 134 files
```

## 📂 Python Files (Excluding scripts/ Directory)
### `backend/__init__.py`
**Package Initializer**
```python
 
```
### `backend/endpoints/__init__.py`
**Package Initializer**
```python
"""
API endpoints for Universal Recycling Purchase Order System
""" 
```
### `backend/twilio/__init__.py`
**Package Initializer**
```python

```
### `backend/utils/__init__.py`
**Package Initializer**
```python
"""
Utility functions for Universal Recycling Purchase Order System
""" 
```
### `backend/database.py`
**CREATE TABLE IF NOT EXISTS**
```python
                CREATE TABLE IF NOT EXISTS requesters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)
```
### `backend/endpoints/auth.py`
**Login/Logout Routes**
```python
@router.post("/login")
```
### `backend/endpoints/html_routes.py`
**HTML Routes (Full Content)**
```python
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.database import get_db_connection
import logging

# Logging setup
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Fetch requesters
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
            # Fetch suppliers
            cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
            # Fetch items
            cursor.execute("SELECT item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
            # Fetch projects
            cursor.execute("SELECT project_code, project_name FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
            # Fetch business details
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            row = cursor.fetchone()
            business_details = dict(row) if row else {
                "company_name": "Universal Recycling Company Pty Ltd",
                "address_line1": "123 Industrial Road",
                "address_line2": "Unit 4",
                "city": "Cape Town",
                "province": "Western Cape",
                "postal_code": "8001",
                "telephone": "+27 21 555 1234",
                "vat_number": "VAT123456789"
            }
            logging.info(f"Business details fetched: {business_details}")

        return templates.TemplateResponse(
            "new_order.html",
            {
                "request": request,
                "requesters": requesters,
                "suppliers": suppliers,
                "items": items,
                "projects": projects,
                "business_details": business_details
            }
        )
    except Exception as e:
        logging.error(f"Error rendering new order page: {str(e)}")
        raise

@router.get("/orders/pending_orders", response_class=HTMLResponse)
async def pending_orders_page(request: Request):
    try:
        return templates.TemplateResponse(
            "pending_orders.html",
            {"request": request}
        )
    except Exception as e:
        logging.error(f"Error rendering pending orders page: {str(e)}")
        raise
```
### `backend/endpoints/lookups.py`
**Lookup Endpoints (Full Content)**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection
import sqlite3
import logging

# Logging setup
logging.basicConfig(
    filename="logs/lookups_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

router = APIRouter(prefix="/lookups", tags=["lookups"])

@router.get("/users")
def get_users():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, rights FROM users")
        users = [dict(row) for row in cursor.fetchall()]
    return {"users": users}

class UserCreate(BaseModel):
    username: str
    password: str
    rights: str

@router.post("/users")
def create_user(user: UserCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, rights) VALUES (?, ?, ?)",
                (user.username, user.password, user.rights)
            )
            conn.commit()
        return {"status": "User created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET username = ?, rights = ? WHERE id = ?",
                (user.username, user.rights, user_id)
            )
            conn.commit()
        return {"status": "User updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/requesters")
def get_requesters():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM requesters")
        requesters = [dict(row) for row in cursor.fetchall()]
    return {"requesters": requesters}

class RequesterCreate(BaseModel):
    name: str

@router.post("/requesters")
def create_requester(requester: RequesterCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requesters (name) VALUES (?)", (requester.name,))
            conn.commit()
        return {"status": "Requester created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/requesters/{requester_id}")
def update_requester(requester_id: int, requester: RequesterCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE requesters SET name = ? WHERE id = ?", (requester.name, requester_id))
            conn.commit()
        return {"status": "Requester updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/suppliers")
def get_suppliers():
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers = [dict(row) for row in cursor.fetchall()]
        return {"suppliers": suppliers}
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class SupplierCreate(BaseModel):
    name: str

@router.post("/suppliers")
def create_supplier(supplier: SupplierCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO suppliers (name) VALUES (?)", (supplier.name,))
            conn.commit()
        return {"status": "Supplier created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: int, supplier: SupplierCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE suppliers SET name = ? WHERE id = ?", (supplier.name, supplier_id))
            conn.commit()
        return {"status": "Supplier updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/items")
def get_items():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_code, item_description FROM items")
        items = [dict(row) for row in cursor.fetchall()]
    return {"items": items}

class ItemCreate(BaseModel):
    item_code: str
    item_description: str

@router.post("/items")
def create_item(item: ItemCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (item_code, item_description) VALUES (?, ?)",
                (item.item_code, item.item_description)
            )
            conn.commit()
        return {"status": "Item created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE items SET item_code = ?, item_description = ? WHERE id = ?",
                (item.item_code, item.item_description, item_id)
            )
            conn.commit()
        return {"status": "Item updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/projects")
def get_projects():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_code, project_name FROM projects")
        projects = [dict(row) for row in cursor.fetchall()]
    return {"projects": projects}

class ProjectCreate(BaseModel):
    project_code: str
    project_name: str

@router.post("/projects")
def create_project(project: ProjectCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO projects (project_code, project_name) VALUES (?, ?)",
                (project.project_code, project.project_name)
            )
            conn.commit()
        return {"status": "Project created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/projects/{project_id}")
def update_project(project_id: int, project: ProjectCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE projects SET project_code = ?, project_name = ? WHERE id = ?",
                (project.project_code, project.project_name, project_id)
            )
            conn.commit()
        return {"status": "Project updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/settings")
def get_settings():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        settings = dict(cursor.fetchall())
    return settings

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.put("/settings")
def update_setting(setting: SettingUpdate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (setting.key, setting.value))
            conn.commit()
        return {"status": "Setting updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update setting: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/business_details")
def get_business_details():
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            row = cursor.fetchone()
            if not row:
                return {
                    "company_name": "",
                    "address_line1": "",
                    "address_line2": "",
                    "city": "",
                    "province": "",
                    "postal_code": "",
                    "telephone": "",
                    "vat_number": ""
                }
            return dict(row)
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class BusinessDetailsUpdate(BaseModel):
    company_name: str
    address_line1: str
    address_line2: str
    city: str
    province: str
    postal_code: str
    telephone: str
    vat_number: str

@router.put("/business_details")
def update_business_details(details: BusinessDetailsUpdate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO business_details (
                    id, company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                details.company_name,
                details.address_line1,
                details.address_line2,
                details.city,
                details.province,
                details.postal_code,
                details.telephone,
                details.vat_number
            ))
            conn.commit()
        return {"status": "Business details updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
```
### `backend/endpoints/orders.py`
**Order Management Endpoints (Full Content)**
```python
from fastapi import APIRouter, HTTPException, Request, UploadFile, Form, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import json
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from ..database import create_order, get_setting, update_setting, get_business_details
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items
from backend.twilio.twilio_utils import send_whatsapp_notification, get_order_number_from_phone

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="frontend/templates")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR = Path("data/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

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
        if not current_number:
            current_number = "URC1000"  # Fallback if not set
            update_setting("order_number_start", current_number)
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
            order.order_number = current_order_number
            # Increment the order number for the next order
            next_number = generate_order_number(current_order_number)
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

        where_clause = " AND ".join(filters) if filters else "1=1"

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
            orders = [dict(row) for row in cursor.fetchall()]
            for order in orders:
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
        log_event("new_orders_log.txt", {"action": "fetch_pending_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "pending_orders"})
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

        where_clause = " AND ".join(filters) if filters else "1=1"

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
            orders = [dict(row) for row in cursor.fetchall()]
            for order in orders:
                order["created_date"] = datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y")
        log_event("new_orders_log.txt", {"action": "fetch_received_orders", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "received_orders"})
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
        log_event("new_orders_log.txt", {"action": "fetch_items_for_order", "order_id": order_id, "count": len(items)})
        return {"items": items}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "items_for_order"})
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
            orders = [dict(row) for row in cursor.fetchall()]
            for order in orders:
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
        log_event("new_orders_log.txt", {"action": "fetch_audit_trail", "count": len(orders)})
        return {"orders": orders}
    except sqlite3.OperationalError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_query", "query": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "audit_trail"})
        raise HTTPException(status_code=500, detail=f"Failed to load audit trail: {e}")

class OrderPDF(BaseModel):
    order_number: str
    date: str
    supplier_id: int
    note_to_supplier: Optional[str]
    items: List[dict]
    total: float
    business_details: dict

@router.post("/generate_pdf")
def generate_pdf(order: OrderPDF):
    try:
        # Fetch supplier details
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, address_line1, address_line2, address_line3, postal_code
                FROM suppliers
                WHERE id = ?
            """, (order.supplier_id,))
            supplier = cursor.fetchone()
            if not supplier:
                raise HTTPException(status_code=404, detail="Supplier not found")
            supplier_dict = dict(supplier)

        # Generate PDF
        pdf_path = PDF_DIR / f"order_{order.order_number}.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height = A4

        # Header: Business Details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 50, order.business_details.get("company_name", "Universal Recycling Company Pty Ltd"))
        c.setFont("Helvetica", 10)
        y = height - 65
        c.drawString(50, y, order.business_details.get("address_line1", ""))
        if order.business_details.get("address_line2"):
            y -= 15
            c.drawString(50, y, order.business_details.get("address_line2", ""))
        y -= 15
        c.drawString(50, y, f"{order.business_details.get('city', '')}, {order.business_details.get('province', '')} {order.business_details.get('postal_code', '')}")
        y -= 15
        c.drawString(50, y, f"Telephone: {order.business_details.get('telephone', '')}")
        y -= 15
        c.drawString(50, y, f"VAT Number: {order.business_details.get('vat_number', '')}")

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 150, f"Purchase Order {order.order_number}")

        # Order Details
        c.setFont("Helvetica", 10)
        y = height - 180
        c.drawString(50, y, f"Order Date: {order.date}")
        y -= 15
        c.drawString(50, y, f"Supplier: {supplier_dict['name']}")
        y -= 15
        supplier_address = ", ".join(filter(None, [
            supplier_dict.get("address_line1", ""),
            supplier_dict.get("address_line2", ""),
            supplier_dict.get("address_line3", ""),
            supplier_dict.get("postal_code", "")
        ]))
        c.drawString(50, y, f"Supplier Address: {supplier_address}")

        # Items Table
        y -= 40
        c.setFont("Helvetica-Bold", 10)
        headers = ["Stock Code", "Description", "Qty", "Unit Price", "Total"]
        x_positions = [50, 100, 250, 350, 400]
        for i, header in enumerate(headers):
            c.drawString(x_positions[i], y, header)
        y -= 5
        c.line(50, y, width - 50, y)

        c.setFont("Helvetica", 10)
        y -= 15
        for item in order.items:
            c.drawString(x_positions[0], y, item["item_code"])
            c.drawString(x_positions[1], y, item["item_description"][:40])  # Truncate for space
            c.drawString(x_positions[2], y, str(item["qty_ordered"]))
            c.drawString(x_positions[3], y, f"R{item['price']:.2f}")
            c.drawString(x_positions[4], y, f"R{(item['qty_ordered'] * item['price']):.2f}")
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

        # Total and Notes
        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"Total (Excluding Tax): R{order.total:.2f}")
        if order.note_to_supplier:
            y -= 20
            c.setFont("Helvetica", 10)
            c.drawString(50, y, f"Note to Supplier: {order.note_to_supplier}")

        # Footer: Date (repeated as per request)
        y -= 20
        c.drawString(50, y, f"Date: {order.date}")

        c.showPage()
        c.save()

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"order_{order.order_number}.pdf"
        )
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "generate_pdf"})
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

# Remove the old GET endpoint since we're using POST now
# @router.get("/generate_pdf/{order_id}")
# def generate_pdf(order_id: int):
#     ... (removed)
```
### `backend/endpoints/requesters.py`
**Requester Endpoints**
```python
@router.get("")
```
### `backend/endpoints/supplier_lookup.py`
**Supplier Lookup Endpoints**
```python
@router.get("")
```
### `backend/endpoints/supplier_lookup_takealot.py`
**Takealot Supplier Lookup**
```python
@router.get("")
```
### `backend/twilio/twilio_utils.py`
**WhatsApp Notifications (Full Content)**
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
### `backend/utils/order_utils.py`
**Order Utilities**
```python
def generate_order_number(current_number: str) -> str:
    """
    Generate the next order number by splitting off any non‑digit
    prefix (which can now be empty) and incrementing the numeric suffix,
    preserving zero‑padding.
    e.g. URC0001 → URC0002, PO009 → PO010, 0001 → 0002
    """
    m = re.match(r"^(\D*)(\d+)$", current_number)
    if not m:
        # if it doesn't end with digits, just append "1"
        return current_number + "1"
    prefix, digits = m.groups()
    width = len(digits)
    num = int(digits) + 1
    return f"{prefix}{str(num).zfill(width)}"
```
### `backend/main.py`
**FastAPI Application Setup**
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
### `data/orders.py`
**Order Data Logic**
```python

```

## 🗄️ Database Schema (`data/orders.db`)
_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._

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

### Table `business_details`
- `id` (INTEGER), pk=True, nullable
- `company_name` (TEXT), pk=False, not null
- `address_line1` (TEXT), pk=False, nullable
- `address_line2` (TEXT), pk=False, nullable
- `city` (TEXT), pk=False, nullable
- `province` (TEXT), pk=False, nullable
- `postal_code` (TEXT), pk=False, nullable
- `telephone` (TEXT), pk=False, nullable
- `vat_number` (TEXT), pk=False, nullable

## 🌐 Frontend Overview
### HTML Templates (`frontend/templates/`)

#### `index.html`
```html

```

#### `home.html`
```html
<!-- frontend/templates/home.html -->
<html>
  <body>
    <h2>Welcome, {{ username }}</h2>
    <p><a href="/logout">Logout</a></p>
  </body>
</html>


```

#### `audit_trail.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Audit Trail</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
    .status { font-weight: bold; }
    .filters { margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
    .filters label { font-weight: bold; }
    input[type="date"], select {
      padding: 0.4rem;
      font-size: 1rem;
      font-family: monospace;
    }
    button {
      padding: 0.5rem 1rem;
      cursor: pointer;
    }
    .expand-icon, .clip-icon, .eye-icon, .note-icon, .supplier-note-icon {
      cursor: pointer;
      font-size: 1.2rem;
      margin: 0 0.3rem;
      display: inline-block;
    }
    .eye-icon.disabled {
      opacity: 0.3;
      cursor: default;
    }
    .audit-details { margin-top: 0.5rem; padding-left: 2rem; }
  </style>
</head>
<body>
  <h2>Audit Trail</h2>

  <div class="filters">
    <label for="start-date">Start Date:</label>
    <input type="date" id="start-date" />
    <label for="end-date">End Date:</label>
    <input type="date" id="end-date" />
    <label for="filter-requester">Requester:</label>
    <select id="filter-requester"></select>
    <label for="filter-supplier">Supplier:</label>
    <select id="filter-supplier"></select>
    <label for="filter-status">Status:</label>
    <select id="filter-status">
      <option value="All">All</option>
      <option value="Pending">Pending</option>
      <option value="Waiting for Approval">Waiting for Approval</option>
      <option value="Awaiting Authorisation">Awaiting Authorisation</option>
      <option value="Received">Received</option>
    </select>
    <button id="run-btn">Run</button>
    <button id="clear-btn">Clear</button>
  </div>

  <table>
    <thead>
      <tr>
        <th>Request Date</th>
        <th>Order Number</th>
        <th>Requester</th>
        <th>Supplier</th>
        <th>Total</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody id="audit-body"></tbody>
  </table>

  <script type="module" src="/static/js/audit_trail.js"></script>
</body>
</html>
```

#### `login.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login - Universal Recycling</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f3f3;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 0 12px rgba(0,0,0,0.1);
            width: 300px;
        }
        h2 {
            margin-bottom: 1rem;
            text-align: center;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.6rem;
            margin: 0.5rem 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 0.6rem;
            background: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form method="post" action="/login">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>

```

#### `print_template.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Printable Order - {{ order.order_number }}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Order {{ order.order_number }}</h1>
    <p><strong>Status:</strong> {{ order.status }}</p>
    <p><strong>Created Date:</strong> {{ order.created_date }}</p>
    <p><strong>Received Date:</strong> {{ order.received_date or "N/A" }}</p>
    <p><strong>Total:</strong> {{ order.total }}</p>
    <p><strong>Requester:</strong> {{ order.requester }}</p>
    <p><strong>Order Note:</strong> {{ order.order_note or "None" }}</p>
    <p><strong>Supplier Note:</strong> {{ order.supplier_note or "None" }}</p>

    <h2>Line Items</h2>
    <table border="1" cellpadding="6" cellspacing="0">
        <thead>
            <tr>
                <th>Item Code</th>
                <th>Description</th>
                <th>Project</th>
                <th>Qty Ordered</th>
                <th>Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.item_code }}</td>
                <td>{{ item.item_description }}</td>
                <td>{{ item.project }}</td>
                <td>{{ item.qty_ordered }}</td>
                <td>{{ item.price }}</td>
                <td>{{ item.total }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>

```

#### `received_orders.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Received Orders</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
    .status { font-weight: bold; }
    .filters { margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
    .filters label { font-weight: bold; }
    input[type="date"], select {
      padding: 0.4rem;
      font-size: 1rem;
      font-family: monospace;
    }
    button {
      padding: 0.5rem 1rem;
      cursor: pointer;
    }
    .expand-icon, .clip-icon, .eye-icon, .note-icon, .supplier-note-icon {
      cursor: pointer;
      font-size: 1.2rem;
      margin: 0 0.3rem;
      display: inline-block;
    }
    .eye-icon.disabled {
      opacity: 0.3;
      cursor: default;
    }
  </style>
</head>
<body>
  <h2>Received Orders</h2>

  <div class="filters">
    <label for="start-date">Start Date:</label>
    <input type="date" id="start-date" />
    <label for="end-date">End Date:</label>
    <input type="date" id="end-date" />
    <label for="filter-requester">Requester:</label>
    <select id="filter-requester"></select>
    <label for="filter-supplier">Supplier:</label>
    <select id="filter-supplier"></select>
    <label for="filter-status">Status:</label>
    <select id="filter-status">
      <option value="All">All</option>
      <option value="Received">Received</option>
    </select>
    <button id="run-btn">Run</button>
    <button id="clear-btn">Clear</button>
  </div>

  <table>
    <thead>
      <tr>
        <th>Request Date</th>
        <th>Order Number</th>
        <th>Requester</th>
        <th>Supplier</th>
        <th>Total</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody id="received-body"></tbody>
  </table>

  <script type="module" src="/static/js/received_orders.js"></script>
</body>
</html>
```

#### `pending_orders.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pending Orders - Universal Recycling</title>
    <link rel="icon" href="data:;base64,=">
    <style>
        body { font-family: Arial, sans-serif; padding: 2rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
        .status { font-weight: bold; }
        .filters { margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
        .filters label { font-weight: bold; }
        input[type="date"], select {
            padding: 0.4rem;
            font-size: 1rem;
            font-family: monospace;
        }
        button {
            padding: 0.5rem 1rem;
            cursor: pointer;
        }
        .expand-icon, .clip-icon, .eye-icon, .note-icon, .supplier-note-icon {
            cursor: pointer;
            font-size: 1.2rem;
            margin: 0 0.3rem;
            display: inline-block;
        }
        .eye-icon.disabled {
            opacity: 0.3;
            cursor: default;
        }
        .details-row table {
            margin: 10px 0;
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <h2>Pending Orders</h2>

    <div class="filters">
        <label for="start-date">Start Date:</label>
        <input type="date" id="start-date">
        <label for="end-date">End Date:</label>
        <input type="date" id="end-date">
        <label for="filter-requester">Requester:</label>
        <select id="filter-requester"></select>
        <label for="filter-supplier">Supplier:</label>
        <select id="filter-supplier"></select>
        <label for="filter-status">Status:</label>
        <select id="filter-status">
            <option value="All">All</option>
            <option value="Pending">Pending</option>
            <option value="Waiting for Approval">Waiting for Approval</option>
            <option value="Awaiting Authorisation">Awaiting Authorisation</option>
            <option value="Authorised">Authorised</option>
        </select>
        <button id="run-btn">Run</button>
        <button id="clear-btn">Clear</button>
    </div>

    <table>
        <thead>
            <tr>
                <th>Request Date</th>
                <th>Order Number</th>
                <th>Requester</th>
                <th>Supplier</th>
                <th>Total</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="pending-body"></tbody>
    </table>

    <script type="module" src="/static/js/pending_orders.js"></script>
</body>
</html>
```

#### `maintenance.html`
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
    <div class="tab" data-tab="business_details">Business Details</div>
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
```

#### `new_order.html`
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
        #note_to_supplier {
            width: 100%;
            height: 150px;
            resize: vertical;
        }
    </style>
</head>
<body>

    <div>
        <h2>Create Purchase Order</h2>
        <div>
            <label>Order Number: <span id="order-number">Loading...</span></label>
        </div>
        <div>
            <label for="request_date">Request Date *</label>
            <input type="date" id="request_date" name="request_date" required>
        </div>
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
                <div id="delivery-address">
                    {{ business_details.company_name }}<br>
                    {{ business_details.address_line1 }}<br>
                    {% if business_details.address_line2 %}
                    {{ business_details.address_line2 }}<br>
                    {% endif %}
                    {{ business_details.city }}, {{ business_details.province }} {{ business_details.postal_code }}<br>
                    Telephone: {{ business_details.telephone }}<br>
                    VAT Number: {{ business_details.vat_number }}
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
            <tbody id="items-body">
            </tbody>
        </table>
        <button type="button" id="add-line">Add Item</button>

        <div>
```

### JavaScript (`frontend/static/js/`)

#### `received_orders.js`
```javascript
import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";
import { loadRequesters, loadSuppliers } from "/static/js/components/shared_filters.js";

function populateDropdown(selectId, items, labelFunc, valueFunc) {
  const dropdown = document.getElementById(selectId);
  dropdown.innerHTML = `<option value="">All</option>`;
  items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = valueFunc(item);
    opt.textContent = labelFunc(item);
    dropdown.appendChild(opt);
  });
}

function escapeHTML(str) {
  if (!str) return "";
  return str.replace(/'/g, "\\'").replace(/"/g, "\\\"").replace(/</g, "<").replace(/>/g, ">").replace(/\n/g, " ").replace(/\r/g, "");
}

function populateTable(data) {
  const tbody = document.getElementById("received-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No received orders found.";
    return;
  }

  data.orders.forEach(order => {
    const row = tbody.insertRow();
    row.setAttribute("data-order-id", order.id);

    const sanitizedOrderNote = escapeHTML(order.order_note || "");
    const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");
    const sanitizedOrderNumber = escapeHTML(order.order_number);
    const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
    const sanitizedRequester = escapeHTML(order.requester);

    row.innerHTML = `
      <td>${order.created_date}</td>
      <td>${sanitizedOrderNumber}</td>
      <td>${sanitizedRequester}</td>
      <td>${sanitizedSupplier}</td>
      <td>R${order.total.toFixed(2)}</td>
      <td>${order.status}</td>
      <td>
        <span class="expand-icon" onclick="window.expandLineItems(${order.id}, this)">⬇️</span>
        <span class="clip-icon" title="View/Upload Attachments" onclick="window.checkAttachments(${order.id}).then(has => has ? window.showViewAttachmentsModal(${order.id}, '${sanitizedOrderNumber}') : window.showUploadAttachmentsModal(${order.id}, '${sanitizedOrderNumber}', () => window.checkAttachments(${order.id}).then(has => this.classList.toggle('eye-icon', has))))">📎</span>
        <span class="note-icon" title="Edit Continuous Order Note" onclick="window.showOrderNoteModal('${sanitizedOrderNote}', ${order.id})">📝</span>
        <span class="supplier-note-icon" title="View Note to Supplier" onclick="try { window.showSupplierNoteModal('${sanitizedSupplierNote}'); } catch (e) { console.error('Failed to show supplier note for order ${order.order_number}:', e); alert('Error displaying supplier note: ' + e.message); }">📦</span>
      </td>
    `;
  });
}

async function loadFiltersAndOrders() {
  try {
    const [suppliersRes, requestersRes] = await Promise.all([
      fetch("/lookups/suppliers").then(res => res.json()),
      fetch("/lookups/requesters").then(res => res.json())
    ]);

    populateDropdown("filter-supplier", suppliersRes.suppliers, s => `${s.account_number} — ${s.name}`, s => s.name);
    populateDropdown("filter-requester", requestersRes.requesters, r => r.name, r => r.name);

    await runFilters();
  } catch (err) {
    console.error("Failed to load filters", err);
  }
}

async function runFilters() {
  const supplierName = document.getElementById("filter-supplier").value;
  const requesterName = document.getElementById("filter-requester").value;
  let startDate = document.getElementById("start-date").value;
  let endDate = document.getElementById("end-date").value;

  const isValidDate = (dateStr) => {
    if (!dateStr) return true;
    const date = new Date(dateStr);
    return !isNaN(date.getTime()) && dateStr === date.toISOString().split("T")[0];
  };

  if (startDate && !isValidDate(startDate)) {
    alert("Invalid start date. Please select a valid date.");
    return;
  }
  if (endDate && !isValidDate(endDate)) {
    alert("Invalid end date. Please select a valid date.");
    return;
  }

  const params = new URLSearchParams();
  if (supplierName) params.append("supplier", supplierName);
  if (requesterName) params.append("requester", requesterName);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/api/received_orders?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch received orders", err);
    alert("Failed to load orders: " + err.message);
  }
}

function clearFilters() {
  document.getElementById("filter-supplier").value = "";
  document.getElementById("filter-requester").value = "";
  document.getElementById("filter-status").value = "";
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  runFilters();
}

document.addEventListener("DOMContentLoaded", () => {
  loadFiltersAndOrders();

  document.getElementById("run-btn").addEventListener("click", runFilters);
  document.getElementById("clear-btn").addEventListener("click", clearFilters);

  // Periodically refresh the received orders table every 30 seconds
  setInterval(runFilters, 30000);
});

window.expandLineItems = expandLineItems;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
```

#### `new_order.js`
```javascript
let itemsList = [];
let projectsList = [];
let rowCount = 0;
let latestOrderId = null;
let latestOrderDetails = null;

function updateGrandTotal() {
    let sum = 0;
    document.querySelectorAll("#items-table tbody tr").forEach(row => {
        const totalField = row.querySelector("td:nth-child(6) input");
        if (totalField) {
            sum += parseFloat(totalField.value) || 0;
        }
    });
    document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

function updateTotal(input) {
    const row = input.closest("tr");
    const index = Array.from(row.parentNode.children).indexOf(row);
    const qty = parseFloat(row.cells[3].querySelector("input").value) || 0;
    const price = parseFloat(row.cells[4].querySelector("input").value) || 0;
    row.cells[5].querySelector("input").value = (qty * price).toFixed(2);
    updateGrandTotal();
}

function autoFillDescription(sel) {
    const desc = sel.selectedOptions[0]?.dataset.description ?? "";
    sel.closest("tr").querySelector("td:nth-child(2) input").value = desc;
}

function deleteRow(btn) {
    if (rowCount > 1) {
        btn.closest("tr").remove();
        rowCount--;
        updateGrandTotal();
    }
}

function addRow() {
    const tbody = document.getElementById("items-body");
    const row = tbody.insertRow();

    const itemOpts = itemsList.map(i =>
        `<option value="${i.item_code}" data-description="${i.item_description}">${i.item_code} — ${i.item_description}</option>`
    ).join("");

    const projOpts = projectsList.map(p =>
        `<option value="${p.project_code}">${p.project_code} — ${p.project_name}</option>`
    ).join("");

    row.innerHTML = `
        <td>
            <select name="items[${rowCount}][item_code]" id="item_code_${rowCount}" onchange="autoFillDescription(this)">
                <option value="">Select Item</option>
                ${itemOpts}
            </select>
        </td>
        <td><input type="text" name="items[${rowCount}][item_description]" id="item_description_${rowCount}" readonly></td>
        <td>
            <select name="items[${rowCount}][project]" id="project_${rowCount}">
                <option value="">Select Project</option>
                ${projOpts}
            </select>
        </td>
        <td><input type="number" name="items[${rowCount}][qty_ordered]" id="qty_ordered_${rowCount}" step="1" min="1" value="1" onchange="updateTotal(this)"></td>
        <td><input type="number" name="items[${rowCount}][price]" id="price_${rowCount}" step="0.01" min="0" value="0" onchange="updateTotal(this)"></td>
        <td><input type="text" name="items[${rowCount}][total]" id="total_${rowCount}" readonly></td>
        <td><button type="button" onclick="deleteRow(this)">Remove</button></td>
    `;
    rowCount++;
    updateGrandTotal();
}

async function loadOrderNumber() {
    try {
        const settingsRes = await fetch("/lookups/settings");
        const settings = await settingsRes.json();
        const orderNumber = settings.order_number_start || "URC1000";
        document.getElementById("order-number").textContent = orderNumber;
        return orderNumber;
    } catch (error) {
        console.error("Error fetching order number:", error);
        document.getElementById("order-number").textContent = "Error";
        return "Error";
    }
}

async function loadDropdowns() {
    try {
        const [supR, reqR, itmR, prjR] = await Promise.all([
            fetch("/lookups/suppliers").then(r => r.json()),
            fetch("/lookups/requesters").then(r => r.json()),
            fetch("/lookups/items").then(r => r.json()),
            fetch("/lookups/projects").then(r => r.json())
        ]);

        const supplierDropdown = document.getElementById("supplier_id");
        supplierDropdown.innerHTML = '<option value="">Select Supplier</option>';
        supR.suppliers.forEach(s => {
```

#### `pending_orders.js`
```javascript
import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";

async function populateDropdown(dropdownId, items, key) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = '<option value="">All</option>';
    if (items && Array.isArray(items)) {
        items.forEach(item => {
            const option = document.createElement("option");
            option.value = item[key];
            option.textContent = item[key];
            dropdown.appendChild(option);
        });
    }
}

function escapeHTML(str) {
    if (!str) return "";
    return str.replace(/'/g, "\\'").replace(/"/g, "\\\"").replace(/</g, "<").replace(/>/g, ">").replace(/\n/g, " ").replace(/\r/g, "");
}

async function fetchData(endpoint) {
    try {
        // Fallback for demo
        if (endpoint === '/lookups/suppliers') {
            return {
                suppliers: [
                    { id: 1, name: "Supplier A" },
                    { id: 2, name: "Supplier B" }
                ]
            };
        }
        const response = await fetch(`http://localhost:8004${endpoint}`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch ${endpoint}: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        return null;
    }
}

async function loadFiltersAndOrders() {
    try {
        const requestersData = await fetchData("/lookups/requesters");
        const suppliersData = await fetchData("/lookups/suppliers");

        await populateDropdown("filter-requester", requestersData?.requesters, "name");
        await populateDropdown("filter-supplier", suppliersData?.suppliers, "name");

        await loadOrders();
    } catch (error) {
        console.error("Failed to load filters:", error);
        await loadOrders();
    }
}

async function loadOrders() {
    try {
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;
        const requester = document.getElementById("filter-requester").value;
        const supplier = document.getElementById("filter-supplier").value;
        const status = document.getElementById("filter-status").value;

        const params = new URLSearchParams();
        if (startDate) params.append("start_date", startDate);
        if (endDate) params.append("end_date", endDate);
        if (requester) params.append("requester", requester);
        if (supplier) params.append("supplier", supplier);
        if (status && status !== "All") params.append("status", status);

        const response = await fetch(`/orders/api/orders/pending_orders?${params.toString()}`, {
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch orders: ${response.status}`);
        }
        const data = await response.json();
        const tbody = document.getElementById("pending-body");
        tbody.innerHTML = "";

        if (data.orders && data.orders.length > 0) {
            data.orders.forEach(order => {
                const row = document.createElement("tr");
                const sanitizedOrderNote = escapeHTML(order.order_note || "");
                const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");
                const sanitizedOrderNumber = escapeHTML(order.order_number);
                const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
                const sanitizedRequester = escapeHTML(order.requester);
                row.innerHTML = `
                    <td>${order.created_date}</td>
                    <td>${sanitizedOrderNumber}</td>
                    <td>${sanitizedRequester}</td>
                    <td>${sanitizedSupplier}</td>
                    <td>R${order.total.toFixed(2)}</td>
                    <td><span class="status">${order.status}</span></td>
                    <td>
                        <span class="expand-icon" onclick="window.expandLineItems(${order.id}, this)">⬇️</span>
                        <span class="clip-icon" title="View/Upload Attachments" onclick="window.checkAttachments(${order.id}).then(has => has ? window.showViewAttachmentsModal(${order.id}, '${sanitizedOrderNumber}') : window.showUploadAttachmentsModal(${order.id}, '${sanitizedOrderNumber}', () => window.checkAttachments(${order.id}).then(has => this.classList.toggle('eye-icon', has))))">📎</span>
                        <span class="eye-icon ${order.status === 'Pending' ? '' : 'disabled'}" title="Receive Order" onclick="${order.status === 'Pending' ? `receiveOrder(${order.id})` : ''}">👁️</span>
                        <span class="note-icon" title="Edit Order Note" onclick="window.showOrderNoteModal('${sanitizedOrderNote}', ${order.id})">📝</span>
                        <span class="supplier-note-icon" title="View Note to Supplier" onclick="try { window.showSupplierNoteModal('${sanitizedSupplierNote}'); } catch (e) { console.error('Failed to show supplier note for order ${order.order_number}:', e); alert('Error displaying supplier note: ' + e.message); }}">📦</span>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="7">No pending orders found.</td></tr>';
        }
    } catch (error) {
        console.error("Error loading orders:", error);
        document.getElementById("pending-body").innerHTML = '<tr><td colspan="7">Error loading orders.</td></tr>';
    }
}

async function receiveOrder(orderId) {
    try {
        const response = await fetch(`/orders/api/items_for_order/${orderId}`, {
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error("Failed to fetch items for receiving");
        }
        const data = await response.json();
        const items = data.items || [];

        const receiveData = [];
        for (const item of items) {
            const qtyReceived = prompt(`Enter quantity received for item ${item.item_code} (Ordered: ${item.qty_ordered}):`, item.qty_received || 0);
            if (qtyReceived === null) continue;
            receiveData.push({
                order_id: orderId,
                item_id: item.id,
                qty_received: parseFloat(qtyReceived) || 0
            });
        }

        if (receiveData.length > 0) {
            const receiveResponse = await fetch("/orders/receive", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(receiveData),
                credentials: 'include'
            });
            if (!receiveResponse.ok) {
                throw new Error("Failed to receive order");
            }
            alert("Order marked as received.");
            await loadOrders();
        }
    } catch (error) {
        console.error("Error receiving order:", error);
        alert("Failed to receive order: " + error.message);
    }
}

function clearFilters() {
    document.getElementById("start-date").value = "";
    document.getElementById("end-date").value = "";
    document.getElementById("filter-requester").value = "";
    document.getElementById("filter-supplier").value = "";
    document.getElementById("filter-status").value = "All";
    loadOrders();
}

// Event listeners
document.getElementById("run-btn").addEventListener("click", loadOrders);
document.getElementById("clear-btn").addEventListener("click", clearFilters);

// Initial load
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);

// Expose functions to global scope for onclick handlers
window.expandLineItems = expandLineItems;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
```

#### `audit_trail.js`
```javascript
import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";
import { loadRequesters, loadSuppliers } from "/static/js/components/shared_filters.js";

function populateDropdown(selectId, items, labelFunc, valueFunc) {
  const dropdown = document.getElementById(selectId);
  dropdown.innerHTML = `<option value="">All</option>`;
  items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = valueFunc(item);
    opt.textContent = labelFunc(item);
    dropdown.appendChild(opt);
  });
}

function escapeHTML(str) {
  if (!str) return "";
  return str.replace(/'/g, "\\'").replace(/"/g, "\\\"").replace(/</g, "<").replace(/>/g, ">").replace(/\n/g, " ").replace(/\r/g, "");
}

function populateTable(data) {
  const tbody = document.getElementById("audit-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No orders found.";
    return;
  }

  data.orders.forEach(order => {
    const row = tbody.insertRow();
    row.setAttribute("data-order-id", order.id);

    const sanitizedOrderNote = escapeHTML(order.order_note || "");
    const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");
    const sanitizedOrderNumber = escapeHTML(order.order_number);
    const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
    const sanitizedRequester = escapeHTML(order.requester);

    row.innerHTML = `
      <td>${order.created_date}</td>
      <td>${sanitizedOrderNumber}</td>
      <td>${sanitizedRequester}</td>
      <td>${sanitizedSupplier}</td>
      <td>R${order.total.toFixed(2)}</td>
      <td>${order.status}</td>
      <td>
        <span class="expand-icon" onclick="window.expandLineItems(${order.id}, this)">⬇️</span>
        <span class="clip-icon" title="View/Upload Attachments" onclick="window.checkAttachments(${order.id}).then(has => has ? window.showViewAttachmentsModal(${order.id}, '${sanitizedOrderNumber}') : window.showUploadAttachmentsModal(${order.id}, '${sanitizedOrderNumber}', () => window.checkAttachments(${order.id}).then(has => this.classList.toggle('eye-icon', has))))">📎</span>
        <span class="note-icon" title="Edit Continuous Order Note" onclick="window.showOrderNoteModal('${sanitizedOrderNote}', ${order.id})">📝</span>
        <span class="supplier-note-icon" title="View Note to Supplier" onclick="try { window.showSupplierNoteModal('${sanitizedSupplierNote}'); } catch (e) { console.error('Failed to show supplier note for order ${order.order_number}:', e); alert('Error displaying supplier note: ' + e.message); }">📦</span>
      </td>
    `;

    // Add audit trail details row
    const auditRow = tbody.insertRow();
    auditRow.style.display = "none";
    auditRow.classList.add(`audit-row-${order.id}`);
    const auditCell = auditRow.insertCell(0);
    auditCell.colSpan = 7;
    auditCell.classList.add("audit-details");

    // Populate audit trail details
    let auditDetails = `
      <strong>Original Order Date:</strong> ${order.created_date}<br>
      <strong>Received Date:</strong> ${order.received_date || 'Not received yet'}<br>
    `;
    if (order.items && order.items.length > 0) {
      auditDetails += "<strong>Items Received:</strong><ul>";
      order.items.forEach(item => {
        auditDetails += `
          <li>
            ${item.item_description} (Code: ${item.item_code})<br>
            Ordered: ${item.qty_ordered}, Received: ${item.qty_received || 0}<br>
            Received Date: ${item.received_date || 'Not received yet'}
          </li>
        `;
      });
      auditDetails += "</ul>";
    }
    auditCell.innerHTML = auditDetails;
  });
}

async function loadFiltersAndOrders() {
  try {
    const [suppliersRes, requestersRes] = await Promise.all([
      fetch("/lookups/suppliers").then(res => res.json()),
      fetch("/lookups/requesters").then(res => res.json())
    ]);

    populateDropdown("filter-supplier", suppliersRes.suppliers, s => `${s.account_number} — ${s.name}`, s => s.name);
    populateDropdown("filter-requester", requestersRes.requesters, r => r.name, r => r.name);

    await runFilters();
  } catch (err) {
```

### Components (`frontend/static/js/components/`)

#### `attachment_modal.js`
```javascript
export function showViewAttachmentsModal(orderId, orderNumber, onUploadComplete = null) {
  fetch(`/orders/attachments/${orderId}`)
    .then(res => res.json())
    .then(data => {
      const files = data.attachments || [];
      const modal = createBaseModal();
      const title = document.createElement("h3");
      title.textContent = `Attachments for ${orderNumber}`;
      modal.inner.appendChild(title);

      if (files.length > 0) {
        const list = document.createElement("ul");
        list.style.listStyle = "none";
        list.style.padding = "0";

        files.forEach(f => {
          const li = document.createElement("li");
          const link = document.createElement("a");
          link.href = `/${f.file_path}`;
          link.textContent = f.filename;
          link.target = "_blank";
          link.style.display = "block";
          link.style.marginBottom = "0.5rem";
          link.style.color = "green";
          link.style.textDecoration = "underline";
          li.appendChild(link);
          list.appendChild(li);
        });

        modal.inner.appendChild(list);
      }

      const dropzone = document.createElement("div");
      dropzone.textContent = "Drag and drop files here or click to select";
      dropzone.style.border = "2px dashed #aaa";
      dropzone.style.padding = "2rem";
      dropzone.style.textAlign = "center";
      dropzone.style.cursor = "pointer";
      dropzone.style.marginTop = "1rem";
      dropzone.style.background = "#fafafa";

      dropzone.onclick = () => {
        const input = document.createElement("input");
        input.type = "file";
        input.multiple = true;
        input.onchange = () => handleFiles(input.files, orderId, modal.inner, onUploadComplete);
        input.click();
      };

      dropzone.ondragover = e => {
        e.preventDefault();
        dropzone.style.background = "#eee";
      };
      dropzone.ondragleave = () => {
        dropzone.style.background = "#fafafa";
      };
      dropzone.ondrop = e => {
        e.preventDefault();
        dropzone.style.background = "#fafafa";
        handleFiles(e.dataTransfer.files, orderId, modal.inner, onUploadComplete);
      };

      modal.inner.appendChild(dropzone);

      const closeBtn = document.createElement("button");
      closeBtn.textContent = "Close";
      closeBtn.style.marginTop = "1.5rem";
      closeBtn.style.padding = "0.5rem 1rem";
      closeBtn.style.border = "none";
      closeBtn.style.cursor = "pointer";
      closeBtn.style.background = "#ccc";
      closeBtn.onclick = () => document.body.removeChild(modal.container);

      modal.inner.appendChild(closeBtn);

      document.body.appendChild(modal.container);
    })
    .catch(err => {
      alert("❌ Failed to load attachments");
      console.error(err);
    });
}

export function showUploadAttachmentsModal(orderId, orderNumber, onUploadComplete = null) {
  showViewAttachmentsModal(orderId, orderNumber, onUploadComplete);
}

export async function checkAttachments(orderId) {
  try {
    const res = await fetch(`/orders/attachments/${orderId}`);
    const data = await res.json();
    return data.attachments && data.attachments.length > 0;
  } catch (err) {
    console.error("Failed to check attachments:", err);
    return false;
  }
}

function handleFiles(fileList, orderId, modalInner, onUploadComplete = null) {
  Array.from(fileList).forEach(file => {
```

#### `expand_line_items.js`
```javascript
export async function expandLineItems(orderId, iconElement) {
  const currentRow = iconElement.closest("tr");
  const existingDetailRow = document.getElementById(`items-row-${orderId}`);

  // Toggle visibility
  if (existingDetailRow) {
    const isHidden = existingDetailRow.style.display === "none";
    existingDetailRow.style.display = isHidden ? "table-row" : "none";
    iconElement.textContent = isHidden ? "⬆️" : "⬇️";
    return;
  }

  try {
    const res = await fetch(`/orders/api/items_for_order/${orderId}`);
    if (!res.ok) throw new Error("Failed to fetch line items");
    const data = await res.json();

    const newRow = document.createElement("tr");
    newRow.id = `items-row-${orderId}`;
    const cell = document.createElement("td");
    cell.colSpan = currentRow.children.length;
    cell.style.padding = "1rem";

    if (!data.items || data.items.length === 0) {
      cell.innerHTML = "<em>No items found for this order.</em>";
    } else {
      const table = document.createElement("table");
      table.style.width = "100%";
      table.style.borderCollapse = "collapse";
      table.style.marginTop = "0.5rem";

      const header = document.createElement("tr");
      header.style.backgroundColor = "#f0f0f0";
      header.style.fontWeight = "bold";
      ["Item Code", "Description", "Project", "Qty", "Price", "Total"].forEach(text => {
        const th = document.createElement("td");
        th.textContent = text;
        header.appendChild(th);
      });
      table.appendChild(header);

      data.items.forEach(item => {
        const row = document.createElement("tr");

        const cells = [
          item.item_code,
          item.item_description,
          item.project,
          item.qty_ordered,
          `R${item.price.toFixed(2)}`,
          `R${(item.qty_ordered * item.price).toFixed(2)}`
        ];

        cells.forEach(text => {
          const td = document.createElement("td");
          td.textContent = text;
          row.appendChild(td);
        });

        table.appendChild(row);
      });

      cell.appendChild(table);
    }

    newRow.appendChild(cell);
    currentRow.parentNode.insertBefore(newRow, currentRow.nextSibling);

    iconElement.textContent = "⬆️";
  } catch (err) {
    console.error("❌ Could not load order line items:", err);
    alert("❌ Could not load order line items");
  }
}

```

#### `shared_filters.js`
```javascript
// Load requesters into a given select element
export async function loadRequesters(selectId) {
    try {
      const res = await fetch("/lookups/requesters");
      const data = await res.json();
      const select = document.getElementById(selectId);
      if (!select) return;
  
      select.innerHTML = '<option value="All">All</option>';
      data.requesters.forEach(r => {
        const opt = document.createElement("option");
        opt.value = r.name;
        opt.textContent = r.name;
        select.appendChild(opt);
      });
    } catch (err) {
      console.error(`❌ Failed to load requesters for ${selectId}:`, err);
    }
  }
  
  // Load suppliers into a given select element
  export async function loadSuppliers(selectId) {
    try {
      const res = await fetch("/lookups/suppliers");
      const data = await res.json();
      const select = document.getElementById(selectId);
      if (!select) return;
  
      select.innerHTML = '<option value="All">All</option>';
      data.suppliers.forEach(s => {
        const opt = document.createElement("option");
        opt.value = s.name;
        opt.textContent = s.name;
        select.appendChild(opt);
      });
    } catch (err) {
      console.error(`❌ Failed to load suppliers for ${selectId}:`, err);
    }
  }
  
```

#### `order_note_modal.js`
```javascript
export function showOrderNoteModal(noteText, orderId) {
  const modal = document.createElement("div");
  modal.className = "note-modal";
  modal.style = `
    position: fixed;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: white;
    border: 1px solid #ccc;
    padding: 2rem;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    z-index: 9999;
    font-family: Arial, sans-serif;
  `;

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "Close";
  closeBtn.style = "float:right; font-weight:bold; cursor:pointer;";
  closeBtn.onclick = () => document.body.removeChild(modal);

  const title = document.createElement("h3");
  title.textContent = "Order Note";

  const noteBox = document.createElement("div");
  noteBox.contentEditable = true;
  noteBox.textContent = noteText || "(No note)";
  noteBox.style = `
    margin-top: 1rem;
    white-space: pre-wrap;
    border: 1px solid #ddd;
    padding: 1rem;
    background: #f9f9f9;
    min-height: 100px;
  `;

  const saveBtn = document.createElement("button");
  saveBtn.textContent = "Save";
  saveBtn.style = "margin-top: 1rem; padding: 0.5rem 1rem; cursor: pointer;";
  saveBtn.onclick = async () => {
    const updatedNote = noteBox.textContent;
    try {
      const res = await fetch(`/orders/save_note/${orderId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_note: updatedNote })
      });
      if (!res.ok) throw new Error("Failed to save order note");
      alert("✅ Order note updated!");
      document.body.removeChild(modal);
    } catch (err) {
      console.error(err);
      alert("❌ Failed to update order note");
    }
  };

  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(noteBox);
  modal.appendChild(saveBtn);
  document.body.appendChild(modal);
}

export function showSupplierNoteModal(noteText) {
  const modal = document.createElement("div");
  modal.className = "note-modal";
  modal.style = `
    position: fixed;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: white;
    border: 1px solid #ccc;
    padding: 2rem;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    z-index: 9999;
    font-family: Arial, sans-serif;
  `;

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "Close";
  closeBtn.style = "float:right; font-weight:bold; cursor:pointer;";
  closeBtn.onclick = () => document.body.removeChild(modal);

  const title = document.createElement("h3");
  title.textContent = "Note to Supplier";

  const noteBox = document.createElement("div");
  noteBox.textContent = noteText || "(No note)";
  noteBox.style = `
    margin-top: 1rem;
    white-space: pre-wrap;
    border: 1px solid #ddd;
    padding: 1rem;
    background: #f9f9f9;
    min-height: 100px;
  `;

```

#### `receive_modal.js`
```javascript
// File: frontend/static/js/components/receive_modal.js

export function showReceiveModal(orderId, orderNumber) {
  fetch(`/orders/api/items_for_order/${orderId}`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch items");
      return res.json();
    })
    .then(data => {
      const modal = document.createElement("div");
      modal.className = "receive-modal";
      modal.style = `
        position: fixed;
        top: 5%;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        max-height: 80%;
        overflow-y: auto;
        background: white;
        border: 1px solid #ccc;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
        z-index: 9999;
      `;

      const closeBtn = document.createElement("button");
      closeBtn.textContent = "X";
      closeBtn.style = "float:right; font-weight:bold; cursor:pointer;";
      closeBtn.onclick = () => document.body.removeChild(modal);

      const title = document.createElement("h3");
      title.textContent = `Mark Order #${orderNumber} as Received`;

      const table = document.createElement("table");
      table.style = "width:100%; border-collapse:collapse; margin-top:1rem;";

      const header = document.createElement("tr");
      ["Item Code", "Description", "Project", "Qty Ordered", "Price", "Total", "Actual Received Qty"].forEach(h => {
        const th = document.createElement("th");
        th.textContent = h;
        th.style.border = "1px solid #ccc";
        header.appendChild(th);
      });
      table.appendChild(header);

      const inputs = [];

      data.items.forEach(item => {
        const row = document.createElement("tr");
        const total = item.qty_ordered * item.price;

        [
          item.item_code,
          item.item_description,
          item.project,
          item.qty_ordered,
          `R${item.price.toFixed(2)}`,
          `R${total.toFixed(2)}`
        ].forEach(text => {
          const td = document.createElement("td");
          td.textContent = text;
          td.style.border = "1px solid #ccc";
          row.appendChild(td);
        });

        const qtyInput = document.createElement("input");
        qtyInput.type = "number";
        qtyInput.min = 0;
        qtyInput.step = 1;
        qtyInput.value = item.qty_ordered;
        qtyInput.style.width = "80px";

        // Use the correct field name for ID
        inputs.push({ itemId: item.id || item.item_id, input: qtyInput });

        const inputTd = document.createElement("td");
        inputTd.style.border = "1px solid #ccc";
        inputTd.appendChild(qtyInput);
        row.appendChild(inputTd);

        table.appendChild(row);
      });

      const submitBtn = document.createElement("button");
      submitBtn.textContent = "Mark as Received";
      submitBtn.style = "margin-top:1rem; padding:0.5rem 1rem; cursor:pointer;";
      submitBtn.onclick = async () => {
        const payload = inputs.map(i => ({
          order_id: orderId,
          item_id: i.itemId,
          qty_received: parseFloat(i.input.value)
        }));

        const res = await fetch("/orders/receive", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

```

## 🌍 Environment Variables (`.env`)
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
FLASK_ENV=development
```

## 📦 Dependencies (`requirements.txt`)
```plaintext
fastapi
uvicorn
jinja2
python-multipart
twilio
python-dotenv

```

## 📜 Logs Overview

### `db_activity_log.txt`
**Recent Entries (Last 20 Lines)**
```plaintext
2025-04-26 12:57:12,718 | INFO | Business details fetched: {'company_name': 'Universal Recycling Company Pty Ltd', 'address_line1': '123 Industrial Road', 'address_line2': 'Unit 4', 'city': 'Cape Town', 'province': 'Western Cape', 'postal_code': '8001', 'telephone': '+27 21 555 1234', 'vat_number': 'VAT123456789'}
2025-04-26 13:03:14,605 | INFO | Database tables created successfully.
2025-04-26 13:03:14,605 | INFO | ✅ Database initialized successfully.
2025-04-26 13:03:18,567 | INFO | Business details fetched: {'company_name': 'Universal Recycling Company Pty Ltd', 'address_line1': '123 Industrial Road', 'address_line2': 'Unit 4', 'city': 'Cape Town', 'province': 'Western Cape', 'postal_code': '8001', 'telephone': '+27 21 555 1234', 'vat_number': 'VAT123456789'}
2025-04-26 13:13:00,607 | INFO | Business details fetched: {'company_name': 'Universal Recycling Company Pty Ltd', 'address_line1': '123 Industrial Road', 'address_line2': 'Unit 4', 'city': 'Cape Town', 'province': 'Western Cape', 'postal_code': '8001', 'telephone': '+27 21 555 1234', 'vat_number': 'VAT123456789'}
2025-04-26 13:22:43,003 | INFO | Database tables created successfully.
2025-04-26 13:22:43,003 | INFO | ✅ Database initialized successfully.
2025-04-26 13:22:51,068 | INFO | Business details fetched: {'company_name': 'Universal Recycling Company Pty Ltd', 'address_line1': '123 Industrial Road', 'address_line2': 'Unit 4', 'city': 'Cape Town', 'province': 'Western Cape', 'postal_code': '8001', 'telephone': '+27 21 555 1234', 'vat_number': 'VAT123456789'}
2025-04-26 13:33:48,938 | INFO | Database tables created successfully.
2025-04-26 13:33:48,938 | INFO | ✅ Database initialized successfully.
2025-04-26 13:33:52,129 | INFO | Business details fetched: {'company_name': 'Universal Recycling Company Pty Ltd', 'address_line1': '123 Industrial Road', 'address_line2': 'Unit 4', 'city': 'Cape Town', 'province': 'Western Cape', 'postal_code': '8001', 'telephone': '+27 21 555 1234', 'vat_number': 'VAT123456789'}
2025-04-26 13:39:53,010 | INFO | Database tables created successfully.
2025-04-26 13:39:53,010 | INFO | ✅ Database initialized successfully.
2025-04-26 13:39:57,559 | INFO | Business details fetched: {'company_name': 'Universal Recycling Company Pty Ltd', 'address_line1': '123 Industrial Road', 'address_line2': 'Unit 4', 'city': 'Cape Town', 'province': 'Western Cape', 'postal_code': '8001', 'telephone': '+27 21 555 1234', 'vat_number': 'VAT123456789'}
2025-04-26 13:46:31,709 | INFO | Database tables created successfully.
2025-04-26 13:46:31,709 | INFO | ✅ Database initialized successfully.
2025-04-26 13:46:40,030 | INFO | Database tables created successfully.
2025-04-26 13:46:40,030 | INFO | ✅ Database initialized successfully.
2025-04-26 13:46:48,672 | INFO | Database tables created successfully.
2025-04-26 13:46:48,672 | INFO | ✅ Database initialized successfully.

```

### `lookups_log.txt`
**Recent Entries (Last 20 Lines)**
```plaintext
{"time": "2025-04-23T06:25:03.098344", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:26:41.592770", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:26:41.593144", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:30:25.787430", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:30:25.787877", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:35:04.784484", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:35:04.784533", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:43:22.431042", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:43:22.431087", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:48:55.141891", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:48:55.141938", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:58:08.411660", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:58:08.411718", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:58:15.727629", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:58:15.727866", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:58:58.279319", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:58:58.279975", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T07:20:21.474724", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T07:20:21.475702", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-23T07:20:21.475731", "endpoint": "/items", "status": "success"}

```

### `message_sid_mapping.json`
**Recent Entries (Last 20 Lines)**
```plaintext
{
  "SM67f65e21b693340d3631975a1d5250e7": "URC1047",
  "SM5e1e5ece690a97a83ceb34827fbd0d60": "URC1047",
  "SM80e490369771e7ce3901073e37149e0a": "URC1047",
  "SMa253731b37feb57569966c5722213e12": "URC1047",
  "SM8be1df91ede905f0f80909396a3e58c0": "URC1047",
  "SM5e451ce0eabf5406419712bc21026acb": "URC1047",
  "SM7fbac78cbd7146216743b4aef1d64ca3": "URC1047",
  "SMc143c42daa4be676a4cdc5bf194e41aa": "URC1049",
  "SMd091b586e9c5b2397767f49e5671fc25": "URC1049",
  "SM0fc57b7c244d65120ec2390caa191379": "URC1049",
  "SM8a0fe84f74951c6f452e66e3c60f6f06": "URC1049",
  "SM34b30c3993132910b240fda432182c9e": "URC1049",
  "SM9b8f9890d3967efca31c4b1e3fb8cb9f": "URC1049",
  "SM72a6aa7400f3678752aeeb6ffb3d74e3": "URC1049"
}
```

### `new_orders_log.txt`
**Recent Entries (Last 20 Lines)**
```plaintext
[2025-04-26T13:42:12.189519] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:42:12.191927] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:43:12.189096] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:43:12.192453] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:44:12.186326] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:44:12.188840] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:45:12.192768] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:45:12.195324] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:46:12.191233] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:46:12.194250] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:47:12.222296] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:47:12.223650] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:48:12.192530] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:48:12.194976] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:49:12.188194] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:49:12.191502] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:50:12.195132] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:50:12.198145] {"action": "fetch_audit_trail", "count": 38}
[2025-04-26T13:51:12.196723] {"action": "fetch_received_orders", "count": 9}
[2025-04-26T13:51:12.199337] {"action": "fetch_audit_trail", "count": 38}

```

### `phone_order_mapping.json`
**Recent Entries (Last 20 Lines)**
```plaintext
{
  "whatsapp:+27645139217": "URC1053",
  "whatsapp:+27834584385": "URC1053",
  "whatsapp:+275387206": "URC1053",
  "whatsapp:+27729186702": "URC1053",
  "whatsapp:+27828249479": "URC1053"
}
```

### `server.log`
**Recent Entries (Last 20 Lines)**
```plaintext
INFO:     Finished server process [61595]
INFO:     Started server process [61602]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [61630] using StatReload
INFO:     Started server process [61636]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50462 - "GET /orders/api/received_orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:50460 - "GET /orders/api/audit_trail HTTP/1.1" 200 OK
INFO:     127.0.0.1:50723 - "GET /orders/api/received_orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:50724 - "GET /orders/api/audit_trail HTTP/1.1" 200 OK
INFO:     127.0.0.1:50991 - "GET /orders/api/received_orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:50992 - "GET /orders/api/audit_trail HTTP/1.1" 200 OK
INFO:     127.0.0.1:51252 - "GET /orders/api/received_orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:51253 - "GET /orders/api/audit_trail HTTP/1.1" 200 OK
INFO:     127.0.0.1:51508 - "GET /orders/api/received_orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:51509 - "GET /orders/api/audit_trail HTTP/1.1" 200 OK

```

### `supplier_lookup_debug.log`
**Recent Entries (Last 20 Lines)**
```plaintext
[2025-04-20T12:40:44.693288]
Fetched URL: https://za.rs-online.com/web/c/?searchTerm=makita
HTTP Status: 200
First 1000 characters of response: <!DOCTYPE html><html lang="en-ZA"><head><meta charSet="utf-8" data-next-head=""/><script data-next-head="">LUX = window.LUX || {};LUX.label = "Search Results Page";</script><title data-next-head="">392 for &#x27;makita&#x27; | RS</title><meta content="width=device-width, initial-scale=1.0" name="viewport" data-next-head=""/><script id="adobe-analytics-script" type="application/javascript" data-next-head="">
    window.rs = window.rs || {"web":{"digitalData":{"customer_contact_id":null,"customer_ship_to":null,"customer_sold_to":null,"customer_type":null,"ecSystemId":"responsive","encryptedUsername":null,"isCreditAccount":null,"jobRole":null,"page_name":"search results page","page_type":"new sr","registrationDate":null,"search_browse":"SEARCH","search_cascade_order":1,"search_categories":0,"search_config":0,"search_interface_name":"","search_keyword":"makita","search_keyword_app":"makita","search_keyword_spell_corrected":"","search_language_used":"en","search_match_mode":"","search_patte... (truncated)

[2025-04-20T12:40:44.724733]
Exception: No matching results found or DOM structure changed

[2025-04-20T12:44:27.434337]
💥 ROUTE HIT: query = makita

[2025-04-20T12:44:27.968844]
Fetched URL: https://www.builders.co.za/search/?text=makita
HTTP Status: 200
First 1000 characters of response: <!DOCTYPE html>
<html lang=en data-appversion=v0.0.1578><head><link href="//accounts.google.com" rel=dns-prefetch /><title>Builders | Shop DIY, Paint and Building Materials Online</title><meta charset=utf-8 /><meta content="initial-scale=1,width=device-width,interactive-widget=resizes-content" name=viewport /><script>var __ZBE__={"uh":"aHR0cHM6Ly93d3cuYnVpbGRlcnMuY28uemE","sc":"R2g2dHVjNkw","ic":"YnVpbGRlcnM","mg":"QUl6YVN5QlI5SzVyZUFNTl9CcFFmbzBBczBfb1UwUWVEWWZpYXdv","icf":"MjU5MjU2MTgyMDIwODM2","ica":"Y28uemEuYnVpbGRlcnMubG9naW4","icg":"MzkzNDAxOTkwODY2LTFrOTBwcWIwamVlM2h1dmhpZWIybnJudjgwdTFiYjJjLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29t",};window.__ZBE__=__ZBE__;</script><link rel=dns-prefetch href="https://www.googletagmanager.com"/><link rel=dns-prefetch href="https://apps.bazaarvoice.com"/><link rel=dns-prefetch href="https://www.google-analytics.com"/><link rel=dns-prefetch href="https://www.googleoptimize.com"/><link rel=dns-prefetch href="https://maps.googleapis.com"/><script>var us... (truncated)

[2025-04-20T12:44:27.971460]
Exception: No products matched or structure changed

```

### `takealot_lookup.log`
**Recent Entries (Last 20 Lines)**
```plaintext
[2025-04-20T13:29:13.205841]
Exception: No products matched or structure changed

[2025-04-20T14:05:10.827015]
Target URL: https://www.takealot.com/all?q=laminator
Scraper URL: http://api.scraperapi.com?api_key=f272c508f0e84b88ac0fa928d4acdda&url=https://www.takealot.com/all?q=laminator
HTTP Status: 401
HTML Preview: Unauthorized request, please make sure your API key is valid.

[2025-04-20T14:05:10.828193]
Exception: ScraperAPI returned 401

[2025-04-20T14:07:09.512596]
Target URL: https://www.takealot.com/all?q=laminator
Scraper URL: http://api.scraperapi.com?api_key=f272c508f0e84b88ac0fa928d4acdda&url=https://www.takealot.com/all?q=laminator
HTTP Status: 401
HTML Preview: Unauthorized request, please make sure your API key is valid.

[2025-04-20T14:07:09.513530]
Exception: ScraperAPI returned 401

```

### `testing_log.txt`
**Recent Entries (Last 20 Lines)**
```plaintext
🚀 Test started
2025-04-19T15:29:15.852963 | 🚀 Running full pipeline integration test...

2025-04-19T15:29:15.861563 | ✅ Order creation succeeded
2025-04-19T15:29:15.861888 | ✅ Line items created in DB
2025-04-19T15:29:15.876258 | ⚠️ Receive response status: 200
2025-04-19T15:29:15.876300 | ⚠️ Response content: {"status":"✅ Order(s) marked as received"}
2025-04-19T15:29:15.876326 | ✅ Order receiving succeeded
2025-04-19T15:29:15.876542 | ✅ Audit trail entries exist
2025-04-19T15:29:15.878922 | ✅ Attachment uploaded
2025-04-19T15:29:15.879134 | ✅ Attachment record exists
2025-04-19T15:29:15.879169 | 
🎉 Pipeline test passed for order URC1017 (ID 21)

```

### `twilio.log`
**Recent Entries (Last 20 Lines)**
```plaintext
2025-04-25 06:50:49,006 | INFO | ✅ Database initialized successfully.
2025-04-25 06:59:42,936 | INFO | ✅ Database initialized successfully.
2025-04-25 07:07:14,423 | INFO | ✅ Database initialized successfully.
2025-04-25 07:08:31,193 | INFO | ✅ Database initialized successfully.
2025-04-25 07:12:07,866 | INFO | ✅ Database initialized successfully.
2025-04-25 07:16:58,775 | INFO | ✅ Database initialized successfully.
=======
2025-04-25 04:41:11,011 | INFO | ✅ Database initialized successfully.
2025-04-25 04:41:38,826 | INFO | ✅ Database initialized successfully.
2025-04-25 04:45:02,559 | INFO | ✅ Database initialized successfully.
2025-04-25 04:58:20,426 | INFO | ✅ Database initialized successfully.
2025-04-25 05:00:48,150 | INFO | ✅ Database initialized successfully.
>>>>>>> Stashed changes
2025-04-25 09:46:44,252 | INFO | ✅ Database initialized successfully.
2025-04-25 16:06:02,504 | INFO | ✅ Database initialized successfully.
2025-04-25 16:07:26,635 | INFO | ✅ Database initialized successfully.
2025-04-25 16:16:26,016 | INFO | ✅ Database initialized successfully.
2025-04-25 17:20:42,293 | INFO | ✅ Database initialized successfully.
2025-04-25 18:23:46,953 | INFO | ✅ Database initialized successfully.
2025-04-25 18:24:26,962 | INFO | ✅ Database initialized successfully.

```

### `whatsapp_log.txt`
**Recent Entries (Last 20 Lines)**
```plaintext
[2025-04-24T06:46:36.722448] {"error": "list index out of range", "type": "webhook"}
[2025-04-24T06:55:12.275257] {"error": "list index out of range", "type": "webhook"}
[2025-04-24T06:58:59.135614] {"action": "received_message", "from": "whatsapp:+27645139217", "message": "authorised", "message_sid": ""}
[2025-04-24T06:58:59.136826] {"error": "No order found for message SID "}
[2025-04-24T07:12:35.280517] {"action": "received_message", "from": "whatsapp:+27645139217", "message": "authorised"}
[2025-04-24T07:12:35.284567] {"action": "order_authorised", "order_number": "URC1051", "from": "whatsapp:+27645139217"}
[2025-04-24T07:19:37.300981] {"action": "received_message", "from": "whatsapp:+27645139217", "message": "like this :"}
[2025-04-24T07:27:59.084904] {"action": "received_message", "from": "whatsapp:+27645139217", "message": "authorised"}
[2025-04-24T07:27:59.088790] {"action": "order_authorised", "order_number": "URC1053", "from": "whatsapp:+27645139217"}

```

## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.


## ⚙️ System Settings

| Key                 | Value   |
|---------------------|---------|
| auth_threshold      | 10000   |
| order_number_start  | URC1024 |
| last_order_number   | URC000  |


## 🚦 FastAPI Endpoint Summary

| Endpoint                     | Method    | Status         |
|------------------------------|-----------|----------------|
| `/orders`                   | POST      | ✅ Implemented |
| `/orders/receive`           | POST      | ✅ Implemented |
| `/orders/next_order_number` | GET       | ✅ Implemented |
| `/attachments/upload`       | POST      | ✅ Implemented |
| `/notes`                    | GET/POST  | ✅ Implemented |
| `/audit`                    | GET       | ⏳ Pending     |
| `/orders/print`             | GET       | ⏳ Planned     |
| `/lookups/suppliers`        | GET       | ✅ Implemented |
| `/lookups/requesters`       | GET       | ✅ Implemented |
| `/lookups/projects`         | GET       | ✅ Implemented |
| `/lookups/items`            | GET       | ✅ Implemented |


## 🧪 Test Coverage Summary

| Test Script | Purpose | Status |
|-------------|---------|--------|
| `test_authorisation_threshold_trigger.py` | High-value order triggers auth flow | ✅ |
| `test_invalid_data_handling.py` | Ensures invalid payloads return 422/400 | ✅ |
| `test_invalid_items_variants.py` | Covers malformed line item edge cases | ✅ |
| `test_pipeline_end_to_end.py` | Full pipeline test: creation → receive | ✅ |
| `test_receive_partial.py` | Tests partial receiving with audit tracking | ✅ |


## ✅ TODOs (Static Manual Items)

- [ ] Modularize long `.js` files into reusable components
- [ ] Finalize `/audit` route with filters + trail UI
- [ ] Finalize `/orders/print` layout + backend
- [ ] Add RBAC (role-based access control)
- [ ] Pagination on long tables (Pending/Received)
- [ ] Security audit on file uploads
- [ ] Normalize filenames and harden upload paths
- [ ] Add upload success/failure status to frontend

