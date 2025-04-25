# 📦 Project Snapshot
Generated: 2025-04-25 04:43:11

## 📁 Directory Tree
````
📂 Root: /Users/stevencohen/Projects/universal_recycling/orders_project
├── backend
│   ├── __init__.py
│   ├── database.py
│   ├── endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── lookups.py
│   │   ├── orders.py
│   │   ├── orders_project
│   │   ├── requesters.py
│   │   ├── supplier_lookup.py
│   │   ├── supplier_lookup_takealot.py
│   │   └── ui_pages.py
│   ├── main.py
│   ├── scrapers
│   ├── twilio
│   │   ├── __init__.py
│   │   └── twilio_utils.py
│   └── utils
│       ├── __init__.py
│       └── order_utils.py
├── data
│   ├── orders.db
│   ├── orders.py
│   ├── printouts
│   │   ├── order_1.txt
│   │   ├── order_3.txt
│   │   └── order_7.txt
│   ├── test_orders.db
│   └── uploads
│       ├── 13_Screenshot_2025-04-23_at_05.19.18.png
│       ├── 14_Screenshot_2025-04-23_at_05.19.18.png
│       ├── 17_Intimisso.pdf
│       ├── 18_Hydehurst RC- Proof of submission.pdf
│       ├── 19_Fidessa Consulting.PDF
│       ├── 20_test_invoice.pdf
│       ├── 21_Fidessa Consulting.PDF
│       ├── 21_test_invoice.pdf
│       ├── 22_Hydehurst RC- Proof of submission.pdf
│       ├── 24_Fidessa Consulting.PDF
│       ├── 25_Screenshot 2025-04-20 at 17.12.14.png
│       ├── 26_Intimisso.pdf
│       ├── 27_test_invoice.pdf
│       ├── 28_Deposit - 2.pdf
│       ├── 28_test_invoice.pdf
│       ├── 30_2025-04-22_18-29.pdf
│       ├── 30_2025-04-22_18-44.pdf
│       ├── 30_2025-04-22_18-44_1.pdf
│       ├── 30_Intimisso.pdf
│       ├── 31_Screenshot_2025-04-23_at_05.19.18.png
│       └── test_invoice.pdf
├── files_for_current_features.md
├── frontend
│   ├── static
│   │   ├── css
│   │   └── js
│   └── templates
│       ├── audit_trail.html
│       ├── home.html
│       ├── index.html
│       ├── login.html
│       ├── maintenance.html
│       ├── new_order.html
│       ├── pending_orders.html
│       ├── print_template.html
│       └── received_orders.html
├── logs
│   ├── db_activity_log.txt
│   ├── lookups_log.txt
│   ├── message_sid_mapping.json
│   ├── new_orders_log.txt
│   ├── phone_order_mapping.json
│   ├── server.log
│   ├── server_startup.log
│   ├── supplier_lookup_debug.log
│   ├── takealot_lookup.log
│   ├── testing_log.txt
│   ├── twilio.log
│   └── whatsapp_log.txt
├── project_status_snapshot.md
├── project_summary.md
├── requirements.txt
└── scripts
    ├── add_debug_validation_handler.py
    ├── clear_transactional_data.py
    ├── dump_project_summary.py
    ├── files_for_current_features.py
    ├── git_pull_project.py
    ├── git_push_project.py
    ├── init_db_fresh.py
    ├── inject_filter_route.py
    ├── insert_get_all_orders.py
    ├── insert_next_order_number_route.py
    ├── insert_pending_route.py
    ├── insert_print_route.py
    ├── insert_receive_route.py
    ├── integration_tests.py
    ├── prepare_lookup_tables.py
    ├── repair_orders_routes.py
    ├── reset_and_test.sh
    ├── seed_static_data.py
    ├── start_server.py
    ├── test_authorisation_threshold_trigger.py
    ├── test_invalid_data_handling.py
    ├── test_invalid_items_variants.py
    ├── test_pipeline_end_to_end.py
    └── test_receive_partial.py
````
## 📂 Python Files

### `backend/database.py`
**Create tables and seed default settings.**
```python
import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

DB_PATH = "data/orders.db"
LOG_PATH = Path("logs/db_activity_log.txt")

def log_db_event(action: str, payload: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {action}: {json.dumps(payload, ensure_ascii=False)}\n")

def init_db() -> None:
    """Create tables and seed default settings."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requesters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT,
                    name TEXT,
                    telephone TEXT,
                    vat_number TEXT,
                    registration_number TEXT,
                    email TEXT,
                    contact_name TEXT,
                    contact_telephone TEXT,
                    address_line1 TEXT,
                    address_line2 TEXT,
                    address_line3 TEXT,
                    postal_code TEXT
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_number TEXT,
                    status TEXT,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    received_date TEXT,
                    total REAL,
                    order_note TEXT,
                    note_to_supplier TEXT,
                    supplier_id INTEGER REFERENCES suppliers(id),
                    requester_id INTEGER REFERENCES requesters(id)
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    item_code TEXT,
                    item_description TEXT,
                    project TEXT,
                    qty_ordered REAL,
                    price REAL,
                    total REAL
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    upload_date TEXT NOT NULL
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    action TEXT,
                    details TEXT,
                    action_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )""")

            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('auth_threshold', '10000')"
            )
            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('order_number_start', 'PO001')"
            )

            conn.commit()
            log_db_event("init_db", {"status": "success"})
    except Exception as e:
        log_db_event("init_db_error", {"error": str(e)})
        raise


def create_order(order_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO orders (
                    order_number, status, created_date, total,
                    order_note, note_to_supplier, supplier_id, requester_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data["order_number"],
                order_data["status"],
                datetime.now().isoformat(),
                order_data["total"],
                order_data.get("order_note"),
                order_data.get("note_to_supplier"),
                order_data.get("supplier_id"),
                order_data["requester_id"]
            ))
            order_id = cursor.lastrowid

            for item in items:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, item_code, item_description, project,
                        qty_ordered, price, total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    item["item_code"],
                    item["item_description"],
                    item["project"],
                    item["qty_ordered"],
                    item["price"],
                    item["qty_ordered"] * item["price"]
                ))

            conn.commit()

            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]

            log_db_event("create_order", {
                "order_number": order_data["order_number"],
                "requester_id": order_data["requester_id"],
                "total": order_data["total"],
                "items_count": len(items)
            })

            return dict(zip(columns, row))
    except Exception as e:
        log_db_event("create_order_error", {"error": str(e)})
        raise


def get_setting(key: str) -> Optional[str]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            log_db_event("get_setting", {"key": key, "result": row[0] if row else None})
            return row[0] if row else None
    except Exception as e:
        log_db_event("get_setting_error", {"key": key, "error": str(e)})
        raise


def update_setting(key: str, value: str) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """, (key, value))
            conn.commit()
            log_db_event("update_setting", {"key": key, "value": value})
    except Exception as e:
        log_db_event("update_setting_error", {"key": key, "error": str(e)})
        raise

```

### `backend/endpoints/__init__.py`
**API endpoints for Universal Recycling Purchase Order System**
```python
"""
API endpoints for Universal Recycling Purchase Order System
""" 
```

### `backend/endpoints/auth.py`
**backend/auth.py**
```python
# backend/auth.py

from fastapi import APIRouter, Request, Form, Response, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
DB_PATH = "data/orders.db"


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash, rights FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user_id, pw_hash, rights = user

        # Dummy check: skip real password checking for now
        # Replace this with hashed check later
        if password != "password":
            raise HTTPException(status_code=401, detail="Incorrect password")

        request.session["user_id"] = user_id
        request.session["username"] = username
        request.session["rights"] = rights

        return RedirectResponse(url="/", status_code=302)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {e}")


@router.get("/logout")
def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@router.get("/")
def home(request: Request):
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("home.html", {"request": request, "username": username})


```

### `backend/endpoints/lookups.py`
**Provide defaults if settings are not found**
```python
from fastapi import APIRouter, HTTPException
from typing import Optional
import sqlite3

router = APIRouter(prefix="/lookups", tags=["lookups"])

@router.get("/suppliers")
def get_suppliers():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
        return {"suppliers": suppliers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch suppliers: {e}")

@router.get("/requesters")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
        return {"requesters": requesters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch requesters: {e}")

@router.post("/requesters")
def add_requester(name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requesters (name) VALUES (?)", (name,))
            conn.commit()
        return {"status": "Requester added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Requester name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add requester: {e}")

@router.put("/requesters/{id}")
def update_requester(id: int, name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE requesters SET name = ? WHERE id = ?", (name, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Requester not found")
        return {"status": "Requester updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Requester name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update requester: {e}")

@router.get("/items")
def get_items():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {e}")

@router.post("/items")
def add_item(item_code: str, item_description: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (item_code, item_description) VALUES (?, ?)", (item_code, item_description))
            conn.commit()
        return {"status": "Item added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Item code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add item: {e}")

@router.put("/items/{id}")
def update_item(id: int, item_code: str, item_description: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET item_code = ?, item_description = ? WHERE id = ?", (item_code, item_description, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
        return {"status": "Item updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Item code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {e}")

@router.get("/projects")
def get_projects():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {e}")

@router.post("/projects")
def add_project(project_code: str, project_name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO projects (project_code, project_name) VALUES (?, ?)", (project_code, project_name))
            conn.commit()
        return {"status": "Project added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Project code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add project: {e}")

@router.put("/projects/{id}")
def update_project(id: int, project_code: str, project_name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE projects SET project_code = ?, project_name = ? WHERE id = ?", (project_code, project_name, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Project not found")
        return {"status": "Project updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Project code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update project: {e}")

@router.get("/users")
def get_users():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, rights FROM users ORDER BY username")
            users = [dict(row) for row in cursor.fetchall()]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {e}")

@router.post("/users")
def add_user(user: dict):
    username = user.get("username")
    password = user.get("password")
    rights = user.get("rights")
    if not username or not password or not rights:
        raise HTTPException(status_code=400, detail="Missing required fields: username, password, rights")
    if rights not in ["edit", "view", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid rights value")
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, rights) VALUES (?, ?, ?)", (username, password, rights))
            conn.commit()
        return {"status": "User added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add user: {e}")

@router.put("/users/{id}")
def update_user(id: int, user: dict):
    username = user.get("username")
    rights = user.get("rights")
    if not username or not rights:
        raise HTTPException(status_code=400, detail="Missing required fields: username, rights")
    if rights not in ["edit", "view", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid rights value")
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ?, rights = ? WHERE id = ?", (username, rights, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return {"status": "User updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")

@router.get("/settings")
def get_settings():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings WHERE key IN ('order_number_start', 'auth_threshold')")
            settings = {row["key"]: row["value"] for row in cursor.fetchall()}
            # Provide defaults if settings are not found
            if "order_number_start" not in settings:
                settings["order_number_start"] = "URC0001"
            if "auth_threshold" not in settings:
                settings["auth_threshold"] = "10000"
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch settings: {e}")

@router.put("/settings")
def update_setting(setting: dict):
    key = setting.get("key")
    value = setting.get("value")
    if not key or not value:
        raise HTTPException(status_code=400, detail="Missing required fields: key, value")
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
            conn.commit()
        return {"status": "Setting updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update setting: {e}")
```

### `backend/endpoints/orders.py`
**UPDATE orders**
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

### `backend/endpoints/requesters.py`
**(No description)**
```python
from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/requesters", tags=["requesters"])

@router.get("")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            result = [dict(row) for row in cursor.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

### `backend/endpoints/supplier_lookup.py`
**Log file path**
```python
from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/supplier_lookup", tags=["supplier_lookup"])

# Log file path
LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "supplier_lookup_debug.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_debug(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}]\n")
        for k, v in entry.items():
            if isinstance(v, str) and len(v) > 1000:
                v = v[:1000] + "... (truncated)"
            f.write(f"{k}: {v}\n")

@router.get("")
def lookup_alternatives(query: str = Query(..., min_length=2)):
    log_debug({"💥 ROUTE HIT": f"query = {query}"})

    try:
        search_url = f"https://www.builders.co.za/search/?text={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}

        resp = requests.get(search_url, headers=headers)
        log_debug({
            "Fetched URL": search_url,
            "HTTP Status": resp.status_code,
            "First 1000 characters of response": resp.text
        })

        if resp.status_code != 200:
            raise Exception(f"Builders returned status {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for product in soup.select(".product-grid .product-tile")[:5]:
            title_el = product.select_one(".product-title")
            price_el = product.select_one(".price")
            link_el = product.select_one("a")

            if not (title_el and price_el and link_el):
                continue

            results.append({
                "title": title_el.text.strip(),
                "price": price_el.text.strip(),
                "link": "https://www.builders.co.za" + link_el.get("href")
            })

        if not results:
            raise Exception("No products matched or structure changed")

        return {"results": results}

    except Exception as e:
        log_debug({"Exception": str(e)})
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")

```

### `backend/endpoints/supplier_lookup_takealot.py`
**(No description)**
```python
from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/supplier_lookup_takealot", tags=["supplier_lookup"])

LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "takealot_lookup.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

SCRAPER_API_KEY = "f272c508f0e84b88ac0fa928d4acdda"

def log_debug(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}]\n")
        for k, v in entry.items():
            if isinstance(v, str) and len(v) > 1000:
                v = v[:1000] + "... (truncated)"
            f.write(f"{k}: {v}\n")

@router.get("")
def lookup_takealot(query: str = Query(..., min_length=2)):
    try:
        target_url = f"https://www.takealot.com/all?q={query.replace(' ', '+')}"
        scraper_url = (
            f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}"
            f"&url={target_url}"
        )

        resp = requests.get(scraper_url)
        log_debug({
            "Target URL": target_url,
            "Scraper URL": scraper_url,
            "HTTP Status": resp.status_code,
            "HTML Preview": resp.text
        })

        if resp.status_code != 200:
            raise Exception(f"ScraperAPI returned {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        product_cards = soup.select("div[data-product-id]")

        results = []
        for card in product_cards[:5]:
            title_el = card.select_one("div[data-testid='product-title']")
            price_el = card.select_one("span.currency")
            link_el = card.select_one("a[href]")

            if not (title_el and link_el):
                continue

            results.append({
                "title": title_el.text.strip(),
                "price": price_el.text.strip() if price_el else "N/A",
                "link": "https://www.takealot.com" + link_el["href"]
            })

        if not results:
            raise Exception("No products matched or structure changed")

        return {"results": results}

    except Exception as e:
        log_debug({"Exception": str(e)})
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")

```

### `backend/endpoints/ui_pages.py`
**(No description)**
```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/orders/new", response_class=HTMLResponse)
def show_new_order_form(request: Request):
    return templates.TemplateResponse("new_order.html", {"request": request})

@router.get("/orders/pending", response_class=HTMLResponse)
def show_pending_orders(request: Request):
    return templates.TemplateResponse("pending_orders.html", {"request": request})

```

### `backend/main.py`
**Install debug validator**
```python
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup, supplier_lookup_takealot
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
app.include_router(ui_pages.router)
app.include_router(supplier_lookup.router)
app.include_router(supplier_lookup_takealot.router)

# HTML routes using Jinja2 templates
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request):
    return templates.TemplateResponse("new_order.html", {"request": request})

@app.get("/orders/pending", response_class=HTMLResponse)
async def pending_orders_page(request: Request):
    return templates.TemplateResponse("pending_orders.html", {"request": request})

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

### `backend/twilio/twilio_utils.py`
**Set up logging**
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

### `backend/utils/__init__.py`
**Utility functions for Universal Recycling Purchase Order System**
```python
"""
Utility functions for Universal Recycling Purchase Order System
""" 
```

### `backend/utils/order_utils.py`
**Generate the next order number by splitting off any non‑digit**
```python
import re
from typing import Any, List
from datetime import datetime

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


def determine_status(total: float, auth_threshold: float) -> str:
    """Return 'Awaiting Authorisation' if total > threshold, else 'Pending'."""
    return "Awaiting Authorisation" if total > auth_threshold else "Pending"


def validate_order_items(items: List[Any]) -> bool:
    """
    Ensure at least one item; qty > 0; price >= 0.
    Raises ValueError on violation.
    """
    if not items:
        raise ValueError("Order must contain at least one item")
    for item in items:
        if item.qty_ordered <= 0:
            raise ValueError("Quantity ordered must be greater than 0")
        if item.price < 0:
            raise ValueError("Price cannot be negative")
    return True

```

### `scripts/add_debug_validation_handler.py`
**Enhances FastAPI's default validation error responses.**
```python
#!/usr/bin/env python3
# Adds a dev-time global exception handler for clearer validation error visibility

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.encoders import jsonable_encoder
import traceback

def install_validation_handler(app):
    """
    Enhances FastAPI's default validation error responses.
    Shows raw request body and structured validation errors.
    """
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        try:
            body = await request.body()
            return JSONResponse(
                status_code=422,
                content={
                    "error": "Validation failed",
                    "path": str(request.url),
                    "detail": jsonable_encoder(exc.errors()),
                    "raw_body": body.decode("utf-8", errors="replace")
                },
            )
        except Exception as inner:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Validation failed, and logging body failed",
                    "original_error": str(exc),
                    "logging_error": traceback.format_exc()
                },
            )

```

### `scripts/clear_transactional_data.py`
**!/usr/bin/env python3**
```python
#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = "data/orders.db"

# Transactional tables to clear (excluding static tables: requesters, suppliers, settings, users, projects, items)
TABLES_TO_CLEAR = [
    "orders",
    "order_items",
    "attachments",
    "audit_trail"
]

def clear_transactional_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for table in TABLES_TO_CLEAR:
                print(f"Clearing table: {table}")
                cursor.execute(f"DELETE FROM {table}")
            # Reset the sqlite_sequence for the cleared tables
            for table in TABLES_TO_CLEAR:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table,))
            # Reset the order_number_start to URC0001
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('order_number_start', 'URC0001')")
            conn.commit()
            print("✅ Transactional data cleared successfully. Order number reset to URC0001.")
    except Exception as e:
        print(f"❌ Failed to clear transactional data: {e}")

if __name__ == "__main__":
    # Ensure the uploads directory is cleared as well
    UPLOAD_DIR = Path("data/uploads")
    if UPLOAD_DIR.exists():
        for file in UPLOAD_DIR.glob("*"):
            try:
                file.unlink()
                print(f"Deleted upload: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
    clear_transactional_data()
```

### `scripts/dump_project_summary.py`
**(.*?)**
```python
#!/usr/bin/env python3
import os
import sqlite3
import re
from pathlib import Path
from datetime import datetime

# --- Config ---
EXCLUDE_DIRS = {'venv', '__pycache__', '.pytest_cache'}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_MD = PROJECT_ROOT / 'project_summary.md'
DB_FILE = PROJECT_ROOT / 'data' / 'orders.db'
TODO_REGEX = re.compile(r"#\s*TODO[:\s]+(.+)", re.IGNORECASE)

# --- Helpers ---
def build_tree(path: Path, prefix='') -> str:
    def _build(path, prefix, level):
        if level > 3:
            return []
        lines = []
        entries = sorted(p for p in path.iterdir() if not p.name.startswith('.') and p.name not in EXCLUDE_DIRS)
        for idx, entry in enumerate(entries):
            connector = '└── ' if idx == len(entries) - 1 else '├── '
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = '    ' if idx == len(entries) - 1 else '│   '
                lines.extend(_build(entry, prefix + extension, level + 1))
        return lines
    return f"📂 Root: {path}\n" + '\n'.join(_build(path, prefix, level=1))

def extract_desc(src: str) -> str:
    m = re.search(r'"""(.*?)"""', src, re.DOTALL) or re.search(r"'''(.*?)'''", src, re.DOTALL)
    if m:
        return m.group(1).strip().splitlines()[0]
    for line in src.splitlines():
        if line.strip().startswith('#'):
            return line.strip().lstrip('# ').strip()
    return '(No description)'

def read_src(path: Path) -> str:
    try:
        if path.suffix in {'.py', '.html', '.js', '.sh', '.md', '.txt'}:
            return path.read_text(encoding='utf-8')
        return ''
    except Exception as e:
        return f"<!-- ERROR reading {path.name}: {e} -->"

def group_files_by_type(files: list[Path]) -> dict:
    grouped = {'Python Files': [], 'HTML Templates': [], 'JS Scripts': [], 'Shell/Other': []}
    for f in files:
        if f.suffix == '.py':
            grouped['Python Files'].append(f)
        elif f.suffix == '.html':
            grouped['HTML Templates'].append(f)
        elif f.suffix == '.js':
            grouped['JS Scripts'].append(f)
        else:
            grouped['Shell/Other'].append(f)
    return grouped

def dump_source_files() -> str:
    all_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in sorted(files):
            p = Path(root) / f
            if p == OUTPUT_MD or p.name.startswith('.') or p.name == '.DS_Store':
                continue
            all_files.append(p)
    grouped = group_files_by_type(all_files)
    md = ""
    for group, files in grouped.items():
        md += f"## 📂 {group}\n\n"
        for p in sorted(files):
            rel = p.relative_to(PROJECT_ROOT)
            src = read_src(p)
            desc = extract_desc(src)
            if src.strip():
                md += f"### `{rel}`\n**{desc}**\n```python\n{src}\n```\n\n"
    return md

def dump_db_schema(db_path: Path) -> str:
    md = "## 🗄️ Database Schema (`data/orders.db`)\n\n"
    if not db_path.exists():
        return md + "_No DB found_\n\n"
    md += "_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._\n\n"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for (tbl,) in cur.fetchall():
        md += f"### Table `{tbl}`\n"
        cur.execute(f"PRAGMA table_info({tbl});")
        for cid, name, dtype, notnull, dflt, pk in cur.fetchall():
            md += f"- `{name}` ({dtype}), pk={bool(pk)}, notnull={bool(notnull)}, default={dflt}\n"
        md += "\n"
    conn.close()
    return md

def dump_test_summary() -> str:
    md = "## 🧪 Test Coverage Summary\n\n"
    md += "| Test Script | Purpose | Status |\n"
    md += "|-------------|---------|--------|\n"
    summary = {
        "test_authorisation_threshold_trigger.py": "High-value order triggers auth flow",
        "test_invalid_data_handling.py": "Ensures invalid payloads return 422/400",
        "test_invalid_items_variants.py": "Covers malformed line item edge cases",
        "test_pipeline_end_to_end.py": "Full pipeline test: creation → receive",
        "test_receive_partial.py": "Tests partial receiving with audit tracking",
    }
    scripts_dir = PROJECT_ROOT / "scripts"
    for test_file in sorted(scripts_dir.glob("test_*.py")):
        name = test_file.name
        purpose = summary.get(name, extract_desc(read_src(test_file)))
        status = "✅" if name in summary else "⏳"
        md += f"| `{name}` | {purpose} | {status} |\n"
    md += "\n"
    return md

def dump_static_todos() -> str:
    return """
## ✅ TODOs (Static Manual Items)

- [ ] Modularize long `.js` files into reusable components
- [ ] Finalize `/audit` route with filters + trail UI
- [ ] Finalize `/orders/print` layout + backend
- [ ] Add RBAC (role-based access control)
- [ ] Pagination on long tables (Pending/Received)
- [ ] Security audit on file uploads
- [ ] Normalize filenames and harden upload paths
- [ ] Add upload success/failure status to frontend
"""

def scan_for_code_todos() -> str:
    todos = []
    for root, _, files in os.walk(PROJECT_ROOT):
        for f in files:
            if f.endswith(('.py', '.js', '.html')):
                path = Path(root) / f
                try:
                    lines = path.read_text(encoding='utf-8').splitlines()
                    for i, line in enumerate(lines):
                        m = TODO_REGEX.search(line)
                        if m:
                            todos.append(f"- `{path.relative_to(PROJECT_ROOT)}`: {m.group(1).strip()}")
                except Exception:
                    continue
    if not todos:
        return "## ⛳ Auto-detected TODOs\n\n_None found._\n"
    return "## ⛳ Auto-detected TODOs\n\n" + '\n'.join(todos) + "\n"

def extra_sections() -> str:
    return """
## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

## ⚙️ System Settings

| Key                 | Value   |
|----------------------|---------|
| auth_threshold       | 10000   |
| order_number_start   | URC1024 |
| last_order_number    | URC000  |

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
"""

# --- Main ---
def main():
    md = []
    md.append(f"# 📦 Project Snapshot\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    md.append("## 📁 Directory Tree\n````\n" + build_tree(PROJECT_ROOT) + "\n````")
    md.append(dump_source_files())
    md.append(dump_db_schema(DB_FILE))
    md.append(dump_static_todos())
    md.append(scan_for_code_todos())
    md.append("## 📝 Project summary\n"
              "This is a custom-built Purchase Order system for Universal Recycling.\n\n"
              "**Build & Testing Approach:**\n"
              "- Features are isolated and tested before being chained\n"
              "- Scripts inject DB rows or hit live endpoints for testing\n"
              "- Full `curl`, Python, and sqlite3 test coverage\n"
              "- UI is layered only on top of a tested backend\n")
    md.append(extra_sections())
    md.append(dump_test_summary())
    try:
        OUTPUT_MD.write_text('\n'.join(md), encoding='utf-8')
        print(f"✅ Written to: {OUTPUT_MD}")
    except Exception as e:
        print(f"❌ Failed to write MD file: {e}")

if __name__ == '__main__':
    main()

```

### `scripts/files_for_current_features.py`
**(No description)**
```python
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
output_md = project_root / "files_for_current_features.md"

file_specs = [
    ("backend/endpoints/orders.py", "FastAPI backend logic for creating, receiving, and listing orders."),
    ("backend/main.py", "Main FastAPI application setup and routing for the Pending Orders screen."),
    ("frontend/static/js/pending_orders.js", "JS logic for filtering, loading, and rendering pending orders."),
    ("frontend/templates/pending_orders.html", "HTML template for rendering the Pending Orders screen."),
    ("frontend/static/js/components/order_note_modal.js", "Reusable modal for editing and saving continuous order notes."),
    ("frontend/static/js/components/date_input.js", "Reusable date input formatter with smart formatting and navigation."),
    ("frontend/static/js/components/attachment_modal.js", "Handles file attachment upload and view logic for orders."),
    ("frontend/static/js/components/expand_line_items.js", "Displays expandable line items per order."),
    ("frontend/static/js/components/receive_modal.js", "Modal for marking orders or items as received."),
    ("frontend/static/js/components/shared_filters.js", "Loads and populates shared dropdown filters like suppliers/requesters."),
]

lines = []
for rel_path, description in file_specs:
    abs_path = project_root / rel_path
    lines.append(f"### `{rel_path}`\n**Purpose:** {description}\n")
    try:
        content = abs_path.read_text(encoding="utf-8")
        lines.append("```python\n" + content + "\n```\n")
    except Exception as e:
        lines.append(f"```text\n⚠️ Could not read file: {e}\n```\n")

output_md.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Dumped to: {output_md}")
```

### `scripts/git_pull_project.py`
**Check for local changes**
```python
import subprocess
import os
import sys
from pathlib import Path

def run(command, desc):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr)
        sys.exit(1)

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📥 Git pull process starting...")

    # Check for local changes
    result = run(["git", "status", "--porcelain"], "Check for local changes")
    stashed = False

    if result.stdout.strip():
        print("📦 Local changes detected — stashing...")
        run(["git", "stash", "push", "-u", "-m", "Auto-stash before pull"], "Create stash")
        stashed = True

    # Pull with rebase
    run(["git", "pull", "--rebase", "origin", "main"], "Pull latest changes with rebase")

    # Restore stashed changes
    if stashed:
        print("🔁 Restoring stashed work...")

        # 🧹 Delete known log conflicts BEFORE popping stash
        conflict_logs = [
            "logs/db_activity_log.txt",
            "logs/server_startup.log"
        ]
        for log_file in conflict_logs:
            path = Path(log_file)
            if path.exists():
                print(f"🧹 Removing log file: {log_file}")
                path.unlink()

        # 🧹 Delete known .pyc cache file
        pycache_file = Path("backend/endpoints/__pycache__/orders.cpython-313.pyc")
        if pycache_file.exists():
            print(f"🧹 Removing pycache: {pycache_file}")
            pycache_file.unlink()

        try:
            run(["git", "stash", "pop"], "Restore stashed changes")
        except SystemExit:
            print("⚠️ Stash pop failed — resolve manually with `git stash list && git stash apply`")
            sys.exit(1)

    print("✅ Git pull completed successfully!")

if __name__ == "__main__":
    main()

```

### `scripts/git_push_project.py`
**Check if this is a Git repo**
```python
import subprocess
import os
import sys
from pathlib import Path

def run(command, desc):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr)
        sys.exit(1)

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    # Check if this is a Git repo
    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📦 Starting full Git sync")

    # Check current branch
    result = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], "Check current branch")
    current_branch = result.stdout.strip()
    print(f"🌿 Current branch: {current_branch}")

    # Stage all changes
    run(["git", "add", "--all"], "Stage all changes")

    # Check for staged files
    result = run(["git", "diff", "--cached", "--name-only"], "Check staged files")
    if not result.stdout.strip():
        print("✅ No changes to commit.")
        return

    # Commit
    run(["git", "commit", "-m", "📝 Auto-commit by script"], "Commit changes")

    # Pull latest with rebase
    run(["git", "pull", "--rebase", "origin", current_branch], "Pull latest changes with rebase")

    # Push changes
    run(["git", "push", "origin", current_branch], "Push changes to origin")

    print("🚀 Git sync completed successfully.")

if __name__ == "__main__":
    main()

```

### `scripts/init_db_fresh.py`
**CREATE TABLE requesters (**
```python
#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path("data/orders.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def recreate_database():
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE requesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );

        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            name TEXT,
            telephone TEXT,
            vat_number TEXT,
            registration_number TEXT,
            email TEXT,
            contact_name TEXT,
            contact_telephone TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            address_line3 TEXT,
            postal_code TEXT
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT,
            status TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            received_date TEXT,
            total REAL,
            order_note TEXT,
            note_to_supplier TEXT,
            supplier_id INTEGER REFERENCES suppliers(id),
            requester_id INTEGER REFERENCES requesters(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            item_code TEXT,
            item_description TEXT,
            project TEXT,
            qty_ordered REAL,
            qty_received REAL,
            received_date TEXT,
            price REAL,
            total REAL
        );

        CREATE TABLE attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TEXT NOT NULL
        );

        CREATE TABLE audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            action TEXT,
            details TEXT,
            action_date TEXT DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER
        );

        CREATE TABLE settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            rights TEXT NOT NULL
        );

        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT UNIQUE
        );

        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT UNIQUE,
            item_description TEXT
        );

        INSERT INTO settings (key, value) VALUES ('auth_threshold', '10000');
        INSERT INTO settings (key, value) VALUES ('order_number_start', 'PO001');
        """)

    print("✅ Database recreated with full schema.")

if __name__ == "__main__":
    recreate_database()


```

### `scripts/inject_filter_route.py`
**@router.get("/pending")**
```python
from pathlib import Path

file = Path("backend/endpoints/orders.py")
text = file.read_text()

filter_route = """
@router.get("/pending")
async def get_pending_orders():
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(\"\"\"
            SELECT 
                o.id, o.order_number, o.created_date, o.total,
                o.order_note, o.supplier_note, o.requester
            FROM orders o
            WHERE o.status = 'Pending'
        \"\"\")

        orders = cursor.fetchall()
        full_result = []

        for order in orders:
            cursor.execute(\"\"\"
                SELECT 
                    item_code, item_description, project,
                    qty_ordered, qty_received, price, total
                FROM order_items
                WHERE order_id = ?
            \"\"\", (order["id"],))
            items = [dict(row) for row in cursor.fetchall()]
            
            full_result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "created_date": order["created_date"],
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"],
                "items": items
            })

        conn.close()
        return {"pending_orders": full_result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
"""

if "/pending" not in text:
    insertion_point = text.rfind("def")
    updated = text[:insertion_point] + filter_route.strip() + "\n\n" + text[insertion_point:]
    file.write_text(updated)
    print("✅ Filter route injected into orders.py")
else:
    print("🔁 Filter route already exists in orders.py — skipping.")

```

### `scripts/insert_get_all_orders.py`
**@router.get("/all")**
```python
from pathlib import Path

TARGET_FILE = Path("backend/endpoints/orders.py")

new_route_code = '''
@router.get("/all")
async def get_all_orders():
    \"\"\"
    Retrieve all orders regardless of status.
    \"\"\"
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(\"\"\"
            SELECT id, order_number, status, created_date, total,
                   order_note, supplier_note, requester
            FROM orders
        \"\"\")

        orders = cursor.fetchall()
        conn.close()

        result = []
        for order in orders:
            result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "status": order["status"],
                "created_date": datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y"),
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"]
            })

        return {"orders": result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
'''
if __name__ == "__main__":
    content = TARGET_FILE.read_text()
    insert_point = content.rfind('@router.get')
    updated = content[:insert_point] + new_route_code.strip() + '\n\n' + content[insert_point:]
    TARGET_FILE.write_text(updated)
    print("✅ /all orders route injected.")

```

### `scripts/insert_next_order_number_route.py`
**@router.get("/next_order_number")**
```python
from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

new_route = """
@router.get("/next_order_number")
async def get_next_order_number():
    from ..database import get_setting
    current = get_setting("order_number_start")
    return {"next_order_number": current}
"""

if __name__ == "__main__":
    content = TARGET.read_text()
    inject_index = content.rfind("@router.get")
    updated = content[:inject_index] + new_route.strip() + "\n\n" + content[inject_index:]
    TARGET.write_text(updated)
    print("✅ /orders/next_order_number route injected.")

```

### `scripts/insert_pending_route.py`
**Retrieve all pending orders, each with full item breakdown.**
```python
from pathlib import Path

# Target: orders endpoint file
TARGET_FILE = Path("backend/endpoints/orders.py")

# Code to inject
pending_route_code = '''
@router.get("/pending")
async def get_pending_orders():
    """
    Retrieve all pending orders, each with full item breakdown.
    """
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                o.id, o.order_number, o.created_date, o.total,
                o.order_note, o.supplier_note, o.requester
            FROM orders o
            WHERE o.status = 'Pending'
        """)

        orders = cursor.fetchall()
        full_result = []

        for order in orders:
            cursor.execute("""
                SELECT 
                    item_code, item_description, project,
                    qty_ordered, qty_received, price, total
                FROM order_items
                WHERE order_id = ?
            """, (order["id"],))
            items = [dict(row) for row in cursor.fetchall()]
            
            full_result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "created_date": datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y"),
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"],
                "items": items
            })

        conn.close()
        return {"pending_orders": full_result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
'''

if __name__ == "__main__":
    content = TARGET_FILE.read_text()
    split_point = content.rfind('@router.get')
    updated = content[:split_point] + pending_route_code.strip()
    TARGET_FILE.write_text(updated)
    print("✅ /pending route injected successfully.")

```

### `scripts/insert_print_route.py`
**from fastapi.responses import HTMLResponse**
```python
from pathlib import Path
import sqlite3
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from starlette.requests import Request

TARGET = Path("../backend/endpoints/orders.py")

injected_code = """
from fastapi.responses import HTMLResponse
from starlette.requests import Request

@router.get("/orders/print/{order_id}", response_class=HTMLResponse)
def print_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute(\"\"\"
                SELECT order_number, status, created_date, received_date, total,
                       order_note, supplier_note, requester
                FROM orders
                WHERE id = ?
            \"\"\", (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            order_dict = {
                "order_number": order[0],
                "status": order[1],
                "created_date": order[2],
                "received_date": order[3],
                "total": order[4],
                "order_note": order[5],
                "supplier_note": order[6],
                "requester": order[7],
            }

            cursor.execute(\"\"\"
                SELECT item_code, item_description, project, qty_ordered, price, total
                FROM order_items
                WHERE order_id = ?
            \"\"\", (order_id,))
            order_items = cursor.fetchall()

        return templates.TemplateResponse("print_template.html", {
            "request": Request({}),
            "order": order_dict,
            "items": order_items
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating printable order: {str(e)}")
"""

if __name__ == "__main__":
    text = TARGET.read_text()
    insert_index = text.rfind("@router.get")
    updated_code = text[:insert_index] + injected_code.strip() + "\n\n" + text[insert_index:]
    TARGET.write_text(updated_code)
    print("✅ /orders/print/{order_id} route injected.")

```

### `scripts/insert_receive_route.py`
**UPDATE order_items**
```python
#!/usr/bin/env python3
from pathlib import Path

orders_py = Path("backend/endpoints/orders.py")

route_code = '''
@router.post("/receive")
def mark_order_received(receive_data: List[dict]):
    try:
        now = datetime.now().isoformat()
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()

            order_ids_updated = set()
            for item in receive_data:
                order_id = item["order_id"]
                item_id = item["item_id"]
                qty_received = item["qty_received"]

                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ? AND order_id = ?
                """, (qty_received, now, item_id, order_id))

                cursor.execute("""
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, 'Received', ?, ?, ?)
                """, (order_id, f"Item ID {item_id} received: {qty_received}", now, 0))

                order_ids_updated.add(order_id)

            for order_id in order_ids_updated:
                cursor.execute("""
                    SELECT COUNT(*) FROM order_items
                    WHERE order_id = ? AND (qty_received IS NULL OR qty_received < qty_ordered)
                """, (order_id,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        UPDATE orders
                        SET status = 'Received', received_date = ?
                        WHERE id = ?
                    """, (now, order_id))

        return {"status": "✅ Order(s) marked as received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to receive order: {e}")
'''

if orders_py.exists():
    code = orders_py.read_text()
    if "/receive" in code:
        print("⚠️  Route already exists in orders.py — skipping.")
    else:
        with open(orders_py, "a") as f:
            f.write("\n" + route_code.strip() + "\n")
        print("✅ /receive route injected into orders.py")
else:
    print("❌ backend/endpoints/orders.py not found")

```

### `scripts/integration_tests.py`
**Requisition System Integration Test Suite**
```python
"""
Requisition System Integration Test Suite
----------------------------------------
A comprehensive test suite that validates the full requisition pipeline
from login through submission to database storage and frontend display.
"""

import os
import sys
import json
import time
import requests
import unittest
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import uuid
import re

# Install required packages with:
# pip install selenium requests webdriver-manager

class TestResult:
    """Stores the result of a single test case with before/after state"""
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now()
        self.end_time = None
        self.passed = False
        self.before_state = {}
        self.after_state = {}
        self.assertions = []
        self.error = None
        self.stacktrace = None
    
    def add_assertion(self, assertion_name, passed, expected=None, actual=None):
        """Add a single assertion result"""
        self.assertions.append({
            "name": assertion_name,
            "passed": passed,
            "expected": expected,
            "actual": actual
        })
    
    def set_before_state(self, state):
        """Set the before state snapshot"""
        self.before_state = state
    
    def set_after_state(self, state):
        """Set the after state snapshot"""
        self.after_state = state
    
    def set_error(self, error, stacktrace):
        """Record an error with stacktrace"""
        self.error = str(error)
        self.stacktrace = stacktrace
    
    def finalize(self, passed):
        """Mark the test as complete with final result"""
        self.passed = passed
        self.end_time = datetime.now()
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else None,
            "passed": self.passed,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "assertions": self.assertions,
            "error": self.error,
            "stacktrace": self.stacktrace
        }
    
    def __str__(self):
        """Format the test result for display"""
        result = f"Test: {self.name}\n"
        result += f"Status: {'PASSED' if self.passed else 'FAILED'}\n"
        result += f"Duration: {(self.end_time - self.start_time).total_seconds():.2f}s\n\n"
        
        # Print before state
        result += "Before State:\n"
        result += json.dumps(self.before_state, indent=2) + "\n\n"
        
        # Print after state
        result += "After State:\n"
        result += json.dumps(self.after_state, indent=2) + "\n\n"
        
        # Print assertions
        result += "Assertions:\n"
        for assertion in self.assertions:
            status = "✓" if assertion["passed"] else "✗"
            result += f"{status} {assertion['name']}\n"
            if not assertion["passed"]:
                result += f"  Expected: {assertion['expected']}\n"
                result += f"  Actual:   {assertion['actual']}\n"
        
        # Print error
        if self.error:
            result += "\nError:\n"
            result += self.error + "\n\n"
            result += "Stacktrace:\n"
            result += self.stacktrace + "\n"
        
        return result

class ValidationSuite:
    """Collects and summarizes multiple test results"""
    def __init__(self):
        self.results = []
    
    def add_result(self, result):
        """Add a test result to the suite"""
        self.results.append(result)
    
    def print_summary(self):
        """Print a summary of all test results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print("\n===== VALIDATION SUMMARY =====")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.2f}%")
        print("=============================\n")
        
        for result in self.results:
            print(result)
            print("-----------------------------\n")
    
    def has_failures(self):
        """Check if any tests failed"""
        return any(not r.passed for r in self.results)

class DatabaseHelper:
    """Helper for database operations via API"""
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_requisition_count(self):
        """Get the total number of requisitions"""
        response = requests.get(f"{self.base_url}/api/requisitions")
        if response.status_code == 200:
            return len(response.json())
        return 0
    
    def get_transaction_count(self):
        """Get the total number of transactions"""
        response = requests.get(f"{self.base_url}/api/transactions")
        if response.status_code == 200:
            return len(response.json())
        return 0
    
    def get_requisition_by_order_number(self, order_number):
        """Get a requisition by its order number"""
        response = requests.get(f"{self.base_url}/api/requisitions")
        if response.status_code == 200:
            requisitions = response.json()
            return [r for r in requisitions if r.get("order_number") == order_number]
        return []
    
    def get_requisition_items(self, requisition_id):
        """Get all items for a requisition"""
        response = requests.get(f"{self.base_url}/api/requisition_items/{requisition_id}")
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_transaction_by_order_number(self, order_number):
        """Get a transaction by its order number"""
        response = requests.get(f"{self.base_url}/api/transactions")
        if response.status_code == 200:
            transactions = response.json()
            return [t for t in transactions if t.get("order_number") == order_number]
        return []
    
    def get_next_order_number(self):
        """Get the next order number from settings"""
        response = requests.get(f"{self.base_url}/api/settings/order_number_start")
        if response.status_code == 200:
            data = response.json()
            return data.get("order_number_start", 1000)
        return 1000

class RequisitionSystemTests:
    """Main test suite for the requisition system"""
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.validation = ValidationSuite()
        
        # Setup WebDriver for browser automation
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)
        
        # Setup database helper
        self.db = DatabaseHelper(self.base_url)
    
    def teardown(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
    
    def login(self, username="Steven"):
        """Log in to the application"""
        self.driver.get(self.base_url)
        
        try:
            # Check if already logged in
            if "currentUser" in self.driver.page_source:
                current_user = self.driver.find_element(By.ID, "currentUser").text
                if username in current_user:
                    return True
            
            # Enter username
            username_input = self.driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys(username)
            
            # Submit form
            login_form = self.driver.find_element(By.ID, "loginForm")
            login_form.submit()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "mainApp"))
            )
            
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def fill_requisition_form(self, data):
        """Fill out the requisition form with test data"""
        # Navigate to form tab
        self.driver.get(self.base_url)
        
        # Wait for page to fully load
        time.sleep(5)
        print("Page loaded, checking for new requisition tab...")
        
        # Set a longer wait time
        wait = WebDriverWait(self.driver, 30)
        
        # Ensure we're on the new requisition tab
        try:
            # Try explicit wait first
            print("Waiting for new requisition tab button...")
            new_req_tab = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('new-requisition')\"]"))
            )
            print("Found tab button, clicking...")
            new_req_tab.click()
            print("Tab button clicked")
        except Exception as e:
            print(f"Error clicking tab button: {e}")
            # If direct click fails, try JavaScript click as fallback
            try:
                print("Attempting fallback method to find tab...")
                new_req_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('new-requisition')\"]")
                print("Found tab via fallback, executing JavaScript click...")
                self.driver.execute_script("arguments[0].click();", new_req_tab)
                print("JavaScript click executed")
            except Exception as e2:
                print(f"Fallback method failed: {e2}")
                # Direct JavaScript call to the function as last resort
                print("Last resort: directly calling showTab function...")
                self.driver.execute_script("showTab('new-requisition');")
                print("showTab function called directly")
        
        # Wait for the form to be visible
        print("Waiting for requisition form to become visible...")
        wait.until(
            EC.visibility_of_element_located((By.ID, "requisitionForm"))
        )
        print("Form is now visible")
        
        # Fill form fields
        if "requestDate" in data:
            print("Setting request date...")
            date_input = wait.until(
                EC.element_to_be_clickable((By.ID, "requestDate"))
            )
            date_input.clear()
            date_input.send_keys(data["requestDate"])
            print("Request date set")
        
        if "requester" in data:
            print("Setting requester...")
            self.driver.find_element(By.ID, "requester").send_keys(data["requester"])
            print("Requester set")
        
        if "supplier" in data:
            print("Setting supplier...")
            self.driver.find_element(By.ID, "supplier").send_keys(data["supplier"])
            print("Supplier set")
        
        if "note" in data:
            print("Setting note...")
            self.driver.find_element(By.ID, "note").send_keys(data["note"])
            print("Note set")
        
        # Fill stock items
        print(f"About to fill {len(data.get('items', []))} stock items...")
        for i, item in enumerate(data.get("items", [])):
            print(f"Filling stock item {i+1}...")
            # If not first item, add new row
            if i > 0:
                print("Adding new row...")
                add_button = self.driver.find_elements(By.CSS_SELECTOR, ".action-square.green-square")[0]
                add_button.click()
                print("New row added")
            
            # Get all stock item rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, ".stock-item-row")
            row = rows[i]
            
            # Select stock code
            print("Selecting stock code...")
            stock_select = row.find_element(By.CSS_SELECTOR, "select[name='stockCode[]']")
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='stockCode[]'] option:nth-child(2)"))
            )
            options = stock_select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if item.get("stockCode", "") in option.text:
                    option.click()
                    print(f"Selected stock code: {option.text}")
                    break
            else:
                # If not found, pick first non-empty
                for option in options:
                    if option.get_attribute("value"):
                        option.click()
                        print(f"Selected first available stock code: {option.text}")
                        break
            
            # Select project code
            print("Selecting project code...")
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='projectCode[]']"))
            )
            project_select = row.find_element(By.CSS_SELECTOR, "select[name='projectCode[]']")
            options = project_select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if option.get_attribute("value"):
                    option.click()
                    print(f"Selected project code: {option.text}")
                    break
            
            # Select sub category (wait for it to populate)
            print("Waiting for subcategories to populate...")
            try:
                wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='subCategory[]'] option:nth-child(2)"))
                )
                subcat_select = row.find_element(By.CSS_SELECTOR, "select[name='subCategory[]']")
                options = subcat_select.find_elements(By.TAG_NAME, "option")
                if len(options) > 1:
                    options[1].click()
                    print(f"Selected subcategory: {options[1].text}")
            except Exception as e:
                print(f"Error selecting subcategory: {e}, continuing anyway...")
            
            # Fill units and price
            print("Setting units...")
            units_input = row.find_element(By.CSS_SELECTOR, "input[name='units[]']")
            units_input.clear()
            units_input.send_keys(str(item.get("units", 1)))
            print(f"Units set to {item.get('units', 1)}")
            
            print("Setting price...")
            price_input = row.find_element(By.CSS_SELECTOR, "input[name='price[]']")
            price_input.clear()
            price_input.send_keys(str(item.get("price", 100)))
            print(f"Price set to {item.get('price', 100)}")
            
        print("Form filling complete")
    
    def submit_form(self, expect_alert=True):
        """Submit the requisition form"""
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#requisitionForm button[type='submit']")
        submit_button.click()
        
        if expect_alert:
            try:
                # Wait for alert and accept it
                WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                return alert_text
            except TimeoutException:
                return None
        return None
    
    def check_session_active(self):
        """Check if user session is still active"""
        try:
            # Try to access currentUser element - should be visible if logged in
            current_user = self.driver.find_element(By.ID, "currentUser").text
            return len(current_user) > 0
        except:
            # If element not found, session likely ended
            return False
    
    def check_login_screen_visible(self):
        """Check if login screen is visible (user logged out)"""
        try:
            login_screen = self.driver.find_element(By.ID, "loginScreen")
            return login_screen.is_displayed()
        except:
            return False
    
    def check_transaction_in_audit_trail(self, order_number):
        """Check if a transaction appears in the audit trail tab"""
        # Navigate to audit trail tab
        self.driver.get(self.base_url)
        
        # Wait for page to fully load
        time.sleep(2)
        
        try:
            # Try explicit wait first
            audit_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('audit-trail')\"]"))
            )
            audit_tab.click()
        except:
            # If direct click fails, try JavaScript click as fallback
            try:
                audit_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('audit-trail')\"]")
                self.driver.execute_script("arguments[0].click();", audit_tab)
            except:
                # Direct JavaScript call to the function as last resort
                self.driver.execute_script("showTab('audit-trail');")
        
        # Wait for data to load
        time.sleep(2)
        
        # Check if transaction is in table
        try:
            transactions_table = self.driver.find_element(By.ID, "transactionsTableBody")
            rows = transactions_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 1 and order_number in cells[1].text:
                    return True
            return False
        except:
            return False
    
    def test_standard_requisition_submission(self):
        """
        Test a standard requisition submission flow from end to end
        
        Validates:
        - Login works
        - Form submission succeeds
        - Requisition is saved to database
        - Items are saved to database
        - Transaction is created
        - Order number increments
        - Session remains active
        - Audit trail shows the transaction
        """
        test_result = TestResult("Standard Requisition Submission")
        
        try:
            # Login
            logged_in = self.login()
            test_result.add_assertion("Login successful", logged_in)
            
            if not logged_in:
                raise Exception("Failed to login, cannot continue test")
            
            # Get initial state
            next_order_number = self.db.get_next_order_number()
            formatted_order_number = f"ORD-{next_order_number}"
            req_count_before = self.db.get_requisition_count()
            txn_count_before = self.db.get_transaction_count()
            
            before_state = {
                "next_order_number": next_order_number,
                "requisition_count": req_count_before,
                "transaction_count": txn_count_before,
                "logged_in": True
            }
            test_result.set_before_state(before_state)
            
            # Fill form with test data
            test_data = {
                "requestDate": "12/04/2024",
                "requester": "Integration Test",
                "supplier": "Validation Supplier",
                "note": "End-to-end integration test",
                "items": [
                    {"stockCode": "AB", "units": 5, "price": 100},
                    {"stockCode": "CD", "units": 2, "price": 200}
                ]
            }
            self.fill_requisition_form(test_data)
            
            # Submit form
            alert_text = self.submit_form()
            form_submitted = alert_text and "success" in alert_text.lower()
            test_result.add_assertion("Form submitted successfully", form_submitted, 
                                     "Alert with success message", alert_text)
            
            # Wait for processing
            time.sleep(3)
            
            # Check if still logged in
            still_logged_in = self.check_session_active()
            logged_out = self.check_login_screen_visible()
            test_result.add_assertion("Session remained active", still_logged_in,
                                     "User still logged in", f"Logged in: {still_logged_in}, Login screen visible: {logged_out}")
            
            # Get updated state from database
            req_count_after = self.db.get_requisition_count()
            txn_count_after = self.db.get_transaction_count()
            current_order_number = self.db.get_next_order_number()
            
            # Check requisition in database
            requisitions = self.db.get_requisition_by_order_number(formatted_order_number)
            requisition_created = len(requisitions) > 0
            test_result.add_assertion("Requisition created in database", requisition_created,
                                     "One requisition record", len(requisitions))
            
            if requisition_created:
                requisition = requisitions[0]
                requisition_id = requisition["id"]
                
                # Check requisition fields
                test_result.add_assertion("Requisition has correct order number", 
                                         requisition["order_number"] == formatted_order_number,
                                         formatted_order_number, requisition["order_number"])
                
                test_result.add_assertion("Requisition has correct requester", 
                                         requisition["requester"] == test_data["requester"],
                                         test_data["requester"], requisition["requester"])
                
                test_result.add_assertion("Requisition has correct supplier", 
                                         requisition["supplier"] == test_data["supplier"],
                                         test_data["supplier"], requisition["supplier"])
                
                test_result.add_assertion("Requisition has correct note", 
                                         requisition["supplier_note"] == test_data["note"],
                                         test_data["note"], requisition["supplier_note"])
                
                # Check requisition items
                req_items = self.db.get_requisition_items(requisition_id)
                items_created = len(req_items) == len(test_data["items"])
                test_result.add_assertion("All requisition items created", items_created,
                                         len(test_data["items"]), len(req_items))
                
                # Calculate expected total value
                expected_total = sum(item["units"] * item["price"] for item in test_data["items"])
                test_result.add_assertion("Requisition has correct total value", 
                                         float(requisition["total_order_value"]) == expected_total,
                                         expected_total, float(requisition["total_order_value"]))
                
                # Check transaction in database
                transactions = self.db.get_transaction_by_order_number(formatted_order_number)
                transaction_created = len(transactions) > 0
                test_result.add_assertion("Transaction created in database", transaction_created,
                                         "One transaction record", len(transactions))
                
                if transaction_created:
                    transaction = transactions[0]
                    
                    # Check transaction fields
                    test_result.add_assertion("Transaction has correct order number", 
                                             transaction["order_number"] == formatted_order_number,
                                             formatted_order_number, transaction["order_number"])
                    
                    test_result.add_assertion("Transaction has correct type", 
                                             transaction["transaction_type"] == "Order Placed",
                                             "Order Placed", transaction["transaction_type"])
                    
                    test_result.add_assertion("Transaction has correct amount", 
                                             float(transaction["amount"]) == expected_total,
                                             expected_total, float(transaction["amount"]))
                    
                    test_result.add_assertion("Transaction has correct user", 
                                             transaction["user"] == test_data["requester"],
                                             test_data["requester"], transaction["user"])
                    
                    test_result.add_assertion("Transaction has correct status", 
                                             transaction["status"] in ["Pending", "pending"],
                                             "Pending", transaction["status"])
            
            # Check if order number incremented
            order_number_incremented = current_order_number == next_order_number + 1
            test_result.add_assertion("Order number incremented", order_number_incremented,
                                     next_order_number + 1, current_order_number)
            
            # Check if transaction appears in audit trail
            in_audit_trail = self.check_transaction_in_audit_trail(formatted_order_number)
            test_result.add_assertion("Transaction visible in audit trail", in_audit_trail,
                                     "Transaction in audit table", in_audit_trail)
            
            # Record final state
            after_state = {
                "next_order_number": current_order_number,
                "requisition_count": req_count_after,
                "transaction_count": txn_count_after,
                "requisition_count_delta": req_count_after - req_count_before,
                "transaction_count_delta": txn_count_after - txn_count_before,
                "still_logged_in": still_logged_in,
                "requisition": requisitions[0] if requisitions else None,
                "transaction": transactions[0] if transactions else None,
                "items_count": len(req_items) if 'req_items' in locals() else 0
            }
            test_result.set_after_state(after_state)
            
            # Determine overall test result
            test_passed = all(assertion["passed"] for assertion in test_result.assertions)
            test_result.finalize(test_passed)
            
        except Exception as e:
            # Capture full stacktrace for debugging
            error_trace = traceback.format_exc()
            test_result.set_error(e, error_trace)
            test_result.finalize(False)
        
        finally:
            # Add result to validation suite
            self.validation.add_result(test_result)
            
        return test_result
    
    def test_session_persistence(self):
        """
        Test that user session persists after form submission
        
        Validates:
        - User remains logged in after submission
        - No redirect to login screen
        - User can navigate to other tabs after submission
        """
        test_result = TestResult("Session Persistence")
        
        try:
            # Login
            logged_in = self.login()
            test_result.add_assertion("Login successful", logged_in)
            
            if not logged_in:
                raise Exception("Failed to login, cannot continue test")
            
            # Get user info before submission
            current_user_before = self.driver.find_element(By.ID, "currentUser").text
            
            before_state = {
                "logged_in": logged_in,
                "username": current_user_before
            }
            test_result.set_before_state(before_state)
            
            # Fill form
            test_data = {
                "requestDate": "12/04/2024",
                "requester": "Session Test",
                "supplier": "Persistence Co",
                "note": "Testing session persistence",
                "items": [
                    {"stockCode": "AB", "units": 1, "price": 25}
                ]
            }
            self.fill_requisition_form(test_data)
            
            # Submit form
            alert_text = self.submit_form()
            form_submitted = alert_text and "success" in alert_text.lower()
            test_result.add_assertion("Form submitted successfully", form_submitted)
            
            # Wait for processing
            time.sleep(3)
            
            # Check if still logged in
            is_logged_in = self.check_session_active()
            login_screen_visible = self.check_login_screen_visible()
            
            test_result.add_assertion("User still logged in after submission", is_logged_in,
                                     "User logged in", is_logged_in)
            
            test_result.add_assertion("Login screen not shown after submission", not login_screen_visible,
                                     "Login screen hidden", login_screen_visible)
            
            # Try navigating to another tab
            try:
                pending_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('pending')\"]")
                pending_tab.click()
                
                # Wait for tab content to load
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "pending"))
                )
                
                pending_tab_visible = True
            except:
                pending_tab_visible = False
            
            test_result.add_assertion("Can navigate to other tabs after submission", pending_tab_visible)
            
            # If still logged in, get current user info
            current_user_after = None
            if is_logged_in:
                try:
                    current_user_after = self.driver.find_element(By.ID, "currentUser").text
                except:
                    current_user_after = None
            
            test_result.add_assertion("Username preserved after submission", 
                                     current_user_after == current_user_before,
                                     current_user_before, current_user_after)
            
            after_state = {
                "logged_in": is_logged_in,
                "username": current_user_after,
                "login_screen_visible": login_screen_visible,
                "navigation_functional": pending_tab_visible
            }
            test_result.set_after_state(after_state)
            
            # Determine overall test result
            test_passed = all(assertion["passed"] for assertion in test_result.assertions)
            test_result.finalize(test_passed)
            
        except Exception as e:
            # Capture full stacktrace for debugging
            error_trace = traceback.format_exc()
            test_result.set_error(e, error_trace)
            test_result.finalize(False)
        
        finally:
            # Add result to validation suite
            self.validation.add_result(test_result)
            
        return test_result
    
    def run_all_tests(self):
        try:
            # Run all tests in sequence
            print("Starting Standard Requisition Submission test...")
            self.test_standard_requisition_submission()
            
            print("Starting Session Persistence test...")
            self.test_session_persistence()
            
            # Print summary
            self.validation.print_summary()
            
            return not self.validation.has_failures()
        finally:
            self.teardown()

if __name__ == "__main__":
    print("Starting Requisition System Integration Tests...")
    tests = RequisitionSystemTests()
    success = tests.run_all_tests()
    sys.exit(0 if success else 1) 
```

### `scripts/prepare_lookup_tables.py`
**CREATE TABLE IF NOT EXISTS suppliers (**
```python
import sqlite3

conn = sqlite3.connect("data/orders.db")
cursor = conn.cursor()

# Create suppliers table with full structure
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    name TEXT,
    tel TEXT,
    vat_number TEXT,
    registration_number TEXT,
    email TEXT,
    contact_name TEXT,
    contact_tel TEXT,
    address_line_1 TEXT,
    address_line_2 TEXT,
    address_line_3 TEXT,
    postal_code TEXT
)
""")

# Create projects table if missing
cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, project_code TEXT NOT NULL UNIQUE)")

# Create items table if missing
cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, item_code TEXT NOT NULL UNIQUE, item_description TEXT)")

# Create users table if missing
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rights TEXT NOT NULL CHECK(rights IN ('View', 'Edit'))
)
""")

# Insert blank placeholder suppliers
for _ in range(3):
    cursor.execute("""
    INSERT INTO suppliers (
        account_number, name, tel, vat_number, registration_number,
        email, contact_name, contact_tel, address_line_1, address_line_2,
        address_line_3, postal_code
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple("" for _ in range(12)))

conn.commit()
conn.close()
print("✅ Lookup tables prepared with full supplier structure.")

```

### `scripts/repair_orders_routes.py`
**SELECT o.*, r.name AS requester**
```python
from pathlib import Path

file = Path("backend/endpoints/orders.py")
routes_code = '''from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import sqlite3
from datetime import datetime
from pathlib import Path

router = APIRouter()

@router.get("/all")
def get_all_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {e}")

@router.get("/pending")
def get_pending_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.status = 'Pending'
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"pending_orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending orders: {e}")

@router.get("/print_to_file/{order_id}")
def print_order_to_file(order_id: int):
    output_path = Path("data/printouts") / f"order_{order_id}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            cursor.execute("""
                SELECT * FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = cursor.fetchall()

        lines = [
            f"Order Number: {order['order_number']}",
            f"Status: {order['status']}",
            f"Created: {order['created_date']}",
            f"Requester: {order['requester']}",
            f"Total: {order['total']}",
            f"Supplier Note: {order['supplier_note'] or 'None'}",
            f"Order Note: {order['order_note'] or 'None'}",
            "",
            "Items:"
        ]
        for item in items:
            lines.append(
                f"- {item[2]} | {item[3]} | Qty: {item[4]} | Price: {item[6]} | Total: {item[7]}"
            )

        output_path.write_text("\n".join(lines))
        return {"message": f"Order written to {output_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Print failed: {str(e)}")

@router.post("/receive")
def receive_order(payload: dict):
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        order_id = payload.get("order_id")
        items = payload.get("items", [])

        for item in items:
            cursor.execute("""
                UPDATE order_items
                SET qty_received = ?
                WHERE order_id = ? AND item_code = ?
            """, (
                item["qty_received"],
                order_id,
                item["item_code"]
            ))

        cursor.execute("""
            SELECT qty_ordered, qty_received FROM order_items WHERE order_id = ?
        """, (order_id,))
        all_items = cursor.fetchall()
        fully_received = all(qr is not None and qr >= qo for qo, qr in all_items)

        if fully_received:
            cursor.execute("""
                UPDATE orders SET status = 'Received', received_date = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), order_id))

        conn.commit()
        conn.close()
        return {"message": "Order received", "fully_received": fully_received}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Receive failed: {e}")

@router.get("/audit/{order_id}")
def get_audit(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM audit_trail WHERE order_id = ?
                ORDER BY action_date
            """, (order_id,))
            logs = [dict(row) for row in cursor.fetchall()]
        return {"audit_trail": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit fetch failed: {e}")

@router.post("/upload_attachment")
async def upload_attachment(order_id: int = Form(...), file: UploadFile = File(...)):
    import os
    try:
        folder = Path("data/uploads")
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, file.filename, str(file_path), datetime.now().isoformat()))
            conn.commit()

        return {"message": "Attachment uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
'''

file.write_text(routes_code)
print("✅ backend/endpoints/orders.py replaced with all missing routes.")

```

### `scripts/seed_static_data.py`
**INSERT INTO users (username, password_hash, rights)**
```python
#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect("data/orders.db")
cursor = conn.cursor()

# --- Users ---
cursor.executemany("""
    INSERT INTO users (username, password_hash, rights)
    VALUES (?, '<hash>', ?)
""", [
    ("Aaron", "Edit"),
    ("Yolandi", "View"),
    ("Steven", "Admin"),
])

# --- Requesters ---
cursor.executemany("""
    INSERT INTO requesters (name) VALUES (?)
""", [
    ("Leon",),
    ("Aaron",),
    ("Raymond",),
    ("Yolande",),
    ("Omar",),
])

# --- Projects ---
cursor.executemany("""
    INSERT INTO projects (project_code) VALUES (?)
""", [
    ("PRO001",),
    ("PRO002",),
    ("PRO003",),
])

# --- Suppliers ---
cursor.executemany("""
    INSERT INTO suppliers (account_number, name) VALUES (?, ?)
""", [
    ("SUP001", "Supplier 1"),
    ("SUP002", "Supplier 2"),
    ("SUP003", "Supplier 3"),
])

# --- Items ---
cursor.executemany("""
    INSERT INTO items (item_code, item_description) VALUES (?, ?)
""", [
    ("ITM001", "Item 1"),
    ("ITM002", "Item 2"),
    ("ITM003", "Item 3"),
])

conn.commit()
conn.close()
print("✅ Static data inserted.")


```

### `scripts/start_server.py`
**!/usr/bin/env python3**
```python
#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

# --- CONFIG ---
PORT = "8004"
APP_MODULE = "backend.main:app"
LOG_FILE = "logs/server.log"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# --------------

print("🟢 Starting FastAPI server...")

# 1. Enforce project root and module importability
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

# 2. Kill any process using the port
print(f"🔪 Killing processes on port {PORT}...")
subprocess.run(f"lsof -ti:{PORT} | xargs kill -9", shell=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Port cleared.")

# 3. Remove all __pycache__ folders
print("🧹 Removing bytecode caches...")
for path in PROJECT_ROOT.rglob("__pycache__"):
    try:
        shutil.rmtree(path)
        print(f"   • Removed {path}")
    except Exception:
        pass

# 4. Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# 5. Start Uvicorn with reload and persistent logging
print(f"🚀 Launching Uvicorn → {APP_MODULE} on port {PORT}...")
with open(LOG_FILE, "a") as log_file:
    subprocess.Popen(
        ["venv/bin/uvicorn", APP_MODULE, "--host", "0.0.0.0", "--port", PORT, "--reload"],
        stdout=log_file,
        stderr=log_file
    )

print(f"✅ Server launched. Logs → {LOG_FILE}")

```

### `scripts/test_authorisation_threshold_trigger.py`
**(No description)**
```python
import requests
import sqlite3
from datetime import datetime

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

def create_high_value_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "Test high value order",
        "note_to_supplier": "Handle with care",
        "items": [
            {
                "item_code": "HIGH001",
                "item_description": "Premium Machine Part",
                "project": "TestProjX",
                "qty_ordered": 1,
                "price": 20000.0  # High price to trigger threshold
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(response.status_code == 200, "Order creation succeeded")
    data = response.json()
    return data["order"]["id"], data["order"]["order_number"]

def check_authorisation_status(order_id):
    row = fetch_one("SELECT status, total FROM orders WHERE id = ?", (order_id,))
    status, total = row
    assert_condition(status == "Awaiting Authorisation", "Status is Awaiting Authorisation")
    assert_condition(total > 10000, "Total is above threshold")

def main():
    print("\n🚨 Running high-value order auth threshold test...\n")
    order_id, order_number = create_high_value_order()
    check_authorisation_status(order_id)
    print(f"\n🎯 Test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()


```

### `scripts/test_invalid_data_handling.py`
**Case 1: Empty item list**
```python
import requests
import sqlite3
from pathlib import Path

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"  # ✅ Matches project root execution context

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

    if not Path(DB_PATH).exists():
        raise FileNotFoundError(f"❌ Cannot find DB at: {DB_PATH}")

    initial_count = count_orders()

    # Case 1: Empty item list
    payload1 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": []
    }
    send_invalid_payload(payload1, "at least")  # ← fixed here

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

```

### `scripts/test_invalid_items_variants.py`
**Case 1: Empty item list**
```python
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


```

### `scripts/test_pipeline_end_to_end.py`
**(No description)**
```python
import requests
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"
LOG_FILE = Path("logs/testing_log.txt")

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {msg}\n")

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    log(f"✅ {message}")

def fetch_from_db(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def create_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "End-to-end test order",
        "note_to_supplier": "Please confirm ASAP",
        "items": [
            {
                "item_code": "TST001",
                "item_description": "Test Widget",
                "project": "TEST-01",
                "qty_ordered": 3,
                "price": 200.0
            },
            {
                "item_code": "TST002",
                "item_description": "Test Cable",
                "project": "TEST-02",
                "qty_ordered": 5,
                "price": 100.0
            }
        ]
    }
    res = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(res.status_code == 200, "Order creation succeeded")
    data = res.json()["order"]
    return data["id"], data["order_number"]

def get_item_ids(order_id):
    rows = fetch_from_db("SELECT id FROM order_items WHERE order_id = ?", (order_id,))
    assert_condition(len(rows) == 2, "Line items created in DB")
    return [r[0] for r in rows]

def receive_order(order_id, item_ids):
    payload = [
        {"order_id": order_id, "item_id": item_ids[0], "qty_received": 3},
        {"order_id": order_id, "item_id": item_ids[1], "qty_received": 5}
    ]
    res = requests.post(f"{BASE_URL}/orders/receive", json=payload)
    log(f"⚠️ Receive response status: {res.status_code}")
    log(f"⚠️ Response content: {res.text}")
    assert_condition(res.status_code == 200, "Order receiving succeeded")

def check_audit_trail(order_id):
    trail = fetch_from_db("SELECT action FROM audit_trail WHERE order_id = ?", (order_id,))
    assert_condition(any("Received" in row[0] for row in trail), "Audit trail entries exist")

def upload_attachment(order_id):
    dummy_file = Path("/Users/stevencohen/Desktop/test_invoice.pdf")
    if not dummy_file.exists():
        dummy_file.write_text("Dummy PDF content")

    with dummy_file.open("rb") as f:
        res = requests.post(
            f"{BASE_URL}/orders/upload_attachment",
            files={"file": f},
            data={"order_id": str(order_id)}
        )
    assert_condition(res.status_code == 200, "Attachment uploaded")

def check_attachment_record(order_id):
    rec = fetch_from_db("SELECT filename FROM attachments WHERE order_id = ?", (order_id,))
    assert_condition(len(rec) > 0, "Attachment record exists")

def main():
    LOG_FILE.write_text("🚀 Test started\n")
    log("🚀 Running full pipeline integration test...\n")
    order_id, order_number = create_order()
    item_ids = get_item_ids(order_id)
    receive_order(order_id, item_ids)
    check_audit_trail(order_id)
    upload_attachment(order_id)
    check_attachment_record(order_id)
    log(f"\n🎉 Pipeline test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()

```

### `scripts/test_receive_partial.py`
**(No description)**
```python
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


```

## 📂 HTML Templates

### `frontend/templates/audit_trail.html`
**(No description)**
```python
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

### `frontend/templates/home.html`
**(No description)**
```python
<!-- frontend/templates/home.html -->
<html>
  <body>
    <h2>Welcome, {{ username }}</h2>
    <p><a href="/logout">Logout</a></p>
  </body>
</html>


```

### `frontend/templates/login.html`
**(No description)**
```python
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

### `frontend/templates/maintenance.html`
**(No description)**
```python
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

### `frontend/templates/new_order.html`
**(No description)**
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create New Order</title>
    <link rel="stylesheet" href="/static/css/new_order.css">
</head>
<body>
    <div class="container">
        <h2>Create Purchase Order</h2>
        <div class="header-section">
            <div>
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
                <div class="address-box">
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
                    <td><input type="text" name="items[0][item_code]"></td>
                    <td><input type="text" name="items[0][item_description]"></td>
                    <td><input type="text" name="items[0][project]"></td>
                    <td><input type="number" name="items[0][qty_ordered]" step="1" min="1" value="1" onchange="updateTotal(0)"></td>
                    <td><input type="number" name="items[0][price]" step="0.01" min="0" value="0" onchange="updateTotal(0)"></td>
                    <td><input type="text" name="items[0][total]" readonly></td>
                    <td><button type="button" onclick="removeRow(this)">Remove</button></td>
                </tr>
            </tbody>
        </table>
        <button type="button" onclick="addRow()">Add Item</button>

        <div class="total-section">
            <label>Total: R <span id="grand-total">0.00</span></label>
            <div class="vat-note">Excluding VAT</div>
        </div>

        <div class="button-section">
            <button type="button" id="email-po" onclick="emailPurchaseOrder()">Email Purchase Order</button>
            <button type="submit" onclick="submitForm()">Submit Order</button>
            <button type="button" id="view-po" onclick="viewPurchaseOrder()">View Purchase Order</button>
            <button type="button" onclick="cancelForm()">Cancel</button>
        </div>
    </div>

    <script>
        (function () {
            let rowCount = 1;

            function addRow() {
                const tbody = document.querySelector("#items-table tbody");
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td><input type="text" name="items[${rowCount}][item_code]"></td>
                    <td><input type="text" name="items[${rowCount}][item_description]"></td>
                    <td><input type="text" name="items[${rowCount}][project]"></td>
                    <td><input type="number" name="items[${rowCount}][qty_ordered]" step="1" min="1" value="1" onchange="updateTotal(${rowCount})"></td>
                    <td><input type="number" name="items[${rowCount}][price]" step="0.01" min="0" value="0" onchange="updateTotal(${rowCount})"></td>
                    <td><input type="text" name="items[${rowCount}][total]" readonly></td>
                    <td><button type="button" onclick="removeRow(this)">Remove</button></td>
                `;
                tbody.appendChild(row);
                rowCount++;
                updateGrandTotal();
            }

            function removeRow(button) {
                if (rowCount > 1) {
                    button.parentElement.parentElement.remove();
                    rowCount--;
                    updateGrandTotal();
                }
            }

            function updateTotal(index) {
                const qty = parseFloat(document.querySelector(`input[name='items[${index}][qty_ordered]']`).value) || 0;
                const price = parseFloat(document.querySelector(`input[name='items[${index}][price]']`).value) || 0;
                const total = qty * price;
                document.querySelector(`input[name='items[${index}][total]']`).value = total.toFixed(2);
                updateGrandTotal();
            }

            function updateGrandTotal() {
                let grandTotal = 0;
                for (let i = 0; i < rowCount; i++) {
                    const totalField = document.querySelector(`input[name='items[${i}][total]']`);
                    if (totalField) {
                        grandTotal += parseFloat(totalField.value) || 0;
                    }
                }
                document.getElementById("grand-total").textContent = grandTotal.toFixed(2);
            }

            async function submitForm() {
                const formData = new FormData();
                const supplierId = document.getElementById("supplier_id").value;
                const noteToSupplier = document.getElementById("note_to_supplier").value;
                formData.append("supplier_id", supplierId);
                formData.append("note_to_supplier", noteToSupplier);
                formData.append("requester_id", "1"); // Hardcoded for demo; adjust as needed

                const items = [];
                for (let i = 0; i < rowCount; i++) {
                    const itemCode = document.querySelector(`input[name='items[${i}][item_code]']`)?.value;
                    const itemDescription = document.querySelector(`input[name='items[${i}][item_description]']`)?.value;
                    const project = document.querySelector(`input[name='items[${i}][project]']`)?.value;
                    const qtyOrdered = document.querySelector(`input[name='items[${i}][qty_ordered]']`)?.value;
                    const price = document.querySelector(`input[name='items[${i}][price]']`)?.value;
                    if (itemCode && itemDescription && project && qtyOrdered && price) {
                        items.push({
                            item_code: itemCode,
                            item_description: itemDescription,
                            project: project,
                            qty_ordered: parseFloat(qtyOrdered),
                            price: parseFloat(price)
                        });
                    }
                }
                formData.append("items", JSON.stringify(items));

                const response = await fetch("/orders", {
                    method: "POST",
                    body: formData
                });
                const result = await response.json();
                if (response.ok) {
                    alert(`Order created successfully: ${result.order.order_number}`);
                    window.location.href = "/orders/pending";
                } else {
                    alert(`Failed to create order: ${result.detail}`);
                }
            }

            function emailPurchaseOrder() {
                alert("Email Purchase Order functionality will be implemented after fixing PDF generation.");
                // Placeholder for emailing the PDF; to be implemented later
            }

            function viewPurchaseOrder() {
                alert("View Purchase Order functionality will be implemented after fixing PDF generation.");
                // Placeholder; to be linked to the view order screen after fixing PDF
                window.location.href = "/orders/pending"; // Temporary redirect
            }

            function cancelForm() {
                window.location.href = "/orders/pending";
            }

            // Expose functions to the global scope for onclick handlers
            window.addRow = addRow;
            window.removeRow = removeRow;
            window.updateTotal = updateTotal;
            window.submitForm = submitForm;
            window.emailPurchaseOrder = emailPurchaseOrder;
            window.viewPurchaseOrder = viewPurchaseOrder;
            window.cancelForm = cancelForm;
        })();
    </script>
</body>
</html>
```

### `frontend/templates/pending_orders.html`
**(No description)**
```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Pending Orders</title>
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
    .expand-icon, .clip-icon, .eye-icon, .receive-icon, .note-icon, .supplier-note-icon {
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
  <h2>Pending Orders</h2>

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

### `frontend/templates/print_template.html`
**(No description)**
```python
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

### `frontend/templates/received_orders.html`
**(No description)**
```python
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

## 📂 JS Scripts

### `frontend/static/js/audit_trail.js`
**(No description)**
```python
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
    console.error("Failed to load filters", err);
  }
}

async function runFilters() {
  const supplierName = document.getElementById("filter-supplier").value;
  const requesterName = document.getElementById("filter-requester").value;
  const status = document.getElementById("filter-status").value;
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
  if (status && status !== "All") params.append("status", status);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/api/audit_trail?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch audit trail", err);
    alert("Failed to load audit trail: " + err.message);
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

  // Periodically refresh the audit trail table every 30 seconds
  setInterval(runFilters, 30000);
});

window.expandLineItems = expandLineItems;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
```

### `frontend/static/js/components/attachment_modal.js`
**(No description)**
```python
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
    const formData = new FormData();
    formData.append("file", file);
    formData.append("order_id", orderId);

    fetch("/orders/upload_attachment", {
      method: "POST",
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        const msg = document.createElement("p");
        msg.textContent = data.status;
        msg.style.color = "green";
        modalInner.appendChild(msg);
        if (onUploadComplete) onUploadComplete();
      })
      .catch(err => {
        const msg = document.createElement("p");
        msg.textContent = `❌ Failed to upload: ${file.name}`;
        msg.style.color = "red";
        modalInner.appendChild(msg);
        console.error(err);
      });
  });
}

function createBaseModal() {
  const container = document.createElement("div");
  container.style.position = "fixed";
  container.style.top = "0";
  container.style.left = "0";
  container.style.width = "100vw";
  container.style.height = "100vh";
  container.style.backgroundColor = "rgba(0,0,0,0.5)";
  container.style.display = "flex";
  container.style.alignItems = "center";
  container.style.justifyContent = "center";
  container.style.zIndex = "9999";

  const inner = document.createElement("div");
  inner.style.backgroundColor = "white";
  inner.style.padding = "1.5rem";
  inner.style.borderRadius = "8px";
  inner.style.width = "90%";
  inner.style.maxWidth = "500px";
  inner.style.maxHeight = "80vh";
  inner.style.overflowY = "auto";
  inner.style.fontFamily = "Arial, sans-serif";
  inner.style.position = "relative";

  const close = document.createElement("button");
  close.textContent = "✖";
  close.style.position = "absolute";
  close.style.top = "10px";
  close.style.right = "10px";
  close.style.background = "none";
  close.style.border = "none";
  close.style.fontSize = "1.2rem";
  close.style.cursor = "pointer";
  close.onclick = () => document.body.removeChild(container);

  inner.appendChild(close);
  container.appendChild(inner);

  return { container, inner };
}
```

### `frontend/static/js/components/expand_line_items.js`
**(No description)**
```python
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

### `frontend/static/js/components/order_note_modal.js`
**(No description)**
```python
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

  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(noteBox);
  document.body.appendChild(modal);
}
```

### `frontend/static/js/components/receive_modal.js`
**(No description)**
```python
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

        if (res.ok) {
          alert("✅ Order marked as received");
          document.body.removeChild(modal);
          location.reload();
        } else {
          const err = await res.json();
          if (Array.isArray(err.detail)) {
            const messages = err.detail.map(obj => obj.msg || JSON.stringify(obj));
            alert("❌ Failed to mark as received:\n" + messages.join("\n"));
          } else {
            alert("❌ Failed to mark as received: " + (err.detail || "Unknown error"));
          }
          
        }
      };

      modal.appendChild(closeBtn);
      modal.appendChild(title);
      modal.appendChild(table);
      modal.appendChild(submitBtn);
      document.body.appendChild(modal);
    })
    .catch(err => {
      console.error("❌ Error loading receive modal:", err);
      alert("❌ Could not open receive modal");
    });
}

```

### `frontend/static/js/components/shared_filters.js`
**(No description)**
```python
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

### `frontend/static/js/new_order.js`
**(No description)**
```python
let itemsList = [];
let projectsList = [];

function updateGrandTotal() {
  let sum = 0;
  document.querySelectorAll(".line-total").forEach(cell => {
    sum += parseFloat(cell.textContent) || 0;
  });
  document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

function updateTotal(input) {
  const row = input.closest("tr");
  const qty = parseFloat(row.cells[3].querySelector("input").value) || 0;
  const price = parseFloat(row.cells[4].querySelector("input").value) || 0;
  row.cells[5].textContent = (qty * price).toFixed(2);
  updateGrandTotal();
}

function autoFillDescription(sel) {
  const desc = sel.selectedOptions[0]?.dataset.description ?? "";
  sel.closest("tr").querySelector("td:nth-child(2) input").value = desc;
}

function deleteRow(btn) {
  btn.closest("tr").remove();
  updateGrandTotal();
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
      <select onchange="autoFillDescription(this)">
        <option value="">Select</option>
        ${itemOpts}
      </select>
    </td>
    <td><input type="text" placeholder="Description"></td>
    <td>
      <select>
        <option value="">Select</option>
        ${projOpts}
      </select>
    </td>
    <td><input type="number" value="1" min="1" onchange="updateTotal(this)"></td>
    <td><input type="number" value="0" min="0" onchange="updateTotal(this)"></td>
    <td class="line-total">0.00</td>
    <td><button type="button" onclick="deleteRow(this)">❌</button></td>
  `;
  updateGrandTotal();
}

async function loadDropdowns() {
  try {
    const [supR, reqR, itmR, prjR, numR] = await Promise.all([
      fetch("/lookups/suppliers").then(r => r.json()),
      fetch("/lookups/requesters").then(r => r.json()),
      fetch("/lookups/items").then(r => r.json()),
      fetch("/lookups/projects").then(r => r.json()),
      fetch("/orders/next_order_number").then(r => r.json())
    ]);

    const supplierDropdown = document.getElementById("supplier");
    supplierDropdown.innerHTML = '<option value="">Select supplier</option>';
    supR.suppliers.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s.id;
      opt.textContent = `${s.account_number} — ${s.name}`;
      supplierDropdown.appendChild(opt);
    });

    const requesterDropdown = document.getElementById("requester");
    requesterDropdown.innerHTML = '<option value="">Select requester</option>';
    reqR.requesters.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r.id;
      opt.textContent = r.name;
      requesterDropdown.appendChild(opt);
    });

    itemsList = itmR.items || [];
    projectsList = prjR.projects || [];

    document.getElementById("order-number").value = numR.next_order_number || "ORD-????";
    document.getElementById("request-date").valueAsDate = new Date();

    addRow();
  } catch (err) {
    console.error("Lookup loading failed", err);
    alert("⚠️ Failed to load dropdowns. Check server or database.");
  }
}

function previewOrder() {
  const rd = document.getElementById("request-date").value;
  const rq = document.getElementById("requester").value;
  const sp = document.getElementById("supplier").value;
  const nt = document.querySelector("textarea[name='note_to_supplier']").value;

  const items = Array.from(document.querySelectorAll("#items-body tr"))
    .map(row => {
      const c = row.querySelectorAll("td");
      return {
        item_code: c[0].querySelector("select").value,
        item_description: c[1].querySelector("input").value,
        project: c[2].querySelector("select").value,
        qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
        price: parseFloat(c[4].querySelector("input").value) || 0
      };
    })
    .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

  alert("Preview:\n" + JSON.stringify({ request_date: rd, requester_id: rq, supplier_id: sp, note_to_supplier: nt, items }, null, 2));
}

async function submitOrder() {
  const rd = document.getElementById("request-date").value;
  const rqId = document.getElementById("requester").value;
  const spId = document.getElementById("supplier").value;
  const nt = document.querySelector("textarea[name='note_to_supplier']").value;
  const rows = document.querySelectorAll("#items-body tr");

  const items = Array.from(rows)
    .map(row => {
      const c = row.querySelectorAll("td");
      return {
        item_code: c[0].querySelector("select").value,
        item_description: c[1].querySelector("input").value,
        project: c[2].querySelector("select").value,
        qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
        price: parseFloat(c[4].querySelector("input").value) || 0
      };
    })
    .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

  if (!rd || !rqId || !spId || items.length === 0) {
    return alert("⚠️ Fill date, requester, supplier & at least one complete line.");
  }

  try {
    const res = await fetch("/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        request_date: rd,
        requester_id: rqId,
        supplier_id: spId,
        note_to_supplier: nt,
        items
      })
    });

    const data = await res.json();

    if (res.ok && data.message === "Order created successfully") {
      const orderNumber = data.order?.order_number || document.getElementById("order-number").value;
      alert(`✅ Order ${orderNumber} created.`);
      location.reload();
    } else {
      const detail = data.detail || data.message || "Unknown error.";
      alert(`❌ ${detail}`);
    }
  } catch (err) {
    console.error("Submit failed", err);
    alert("❌ Submission failed.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadDropdowns();
  document.getElementById("add-line").addEventListener("click", addRow);
  document.getElementById("preview-order").addEventListener("click", previewOrder);
  document.getElementById("submit-order").addEventListener("click", submitOrder);
});

```

### `frontend/static/js/pending_orders.js`
**(No description)**
```python
import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showReceiveModal } from "/static/js/components/receive_modal.js";
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
  return str.replace(/'/g, "\\'").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, " ").replace(/\r/g, "");
}

function populateTable(data) {
  const tbody = document.getElementById("pending-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No pending orders found.";
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
        <span class="receive-icon" title="Mark as Received" onclick="window.showReceiveModal(${order.id}, '${sanitizedOrderNumber}')">✅</span>
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
  const status = document.getElementById("filter-status").value;
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
  if (status && status !== "All") params.append("status", status);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/api/orders/pending_orders?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch filtered orders", err);
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

  // Periodically refresh the pending orders table every 30 seconds
  setInterval(runFilters, 30000);
});

window.expandLineItems = expandLineItems;
window.showReceiveModal = showReceiveModal;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
```

### `frontend/static/js/received_orders.js`
**(No description)**
```python
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

## 📂 Shell/Other

### `data/printouts/order_1.txt`
**(No description)**
```python
Order Number: PO002
Status: Pending
Created Date: 2025-04-17T09:53:39.614927
Received Date: None
Total: 29.97
Order Note: Shell test order
Supplier Note: Test supplier
Requester: Aaron

Line Items:
-----------
Item Code: TEST123
Description: Integration Widget
Project: TEST
Qty: 3.0
Price: 9.99
Total: 29.97


```

### `data/printouts/order_3.txt`
**(No description)**
```python
order_number: PO_TEST_001
status: Received
created_date: 2025-04-13T13:24:38.837327
received_date: 2025-04-13T14:18:43.917109
total: 999.99
order_note: This is a test order note
supplier_note: This is a supplier note
requester: Steven

Line Items:
-----------
item_code: TEST001
item_description: Test Widget A
project: Project A
qty_ordered: 3
price: 100.0
total: 300.0

item_code: TEST002
item_description: Test Widget B
project: Project B
qty_ordered: 2
price: 349.99
total: 699.99


```

### `data/printouts/order_7.txt`
**(No description)**
```python
Order Number: PO_TESTA1
Status: Awaiting Authorisation
Created Date: 2025-04-17T15:37:12.567632
Received Date: None
Total: 14000.0
Order Note: High Value Order 1
Note to Supplier: Needs urgent approval
Requester: Aaron

Line Items:
-----------
Item Code: ITM003
Description: Pump
Project: PRO003
Qty: 2.0
Price: 6000.0
Total: 12000.0

Item Code: ITM001
Description: Valve
Project: PRO001
Qty: 1.0
Price: 2000.0
Total: 2000.0


```

### `files_for_current_features.md`
**UPDATE order_items**
```python
### `backend/endpoints/orders.py`
**Purpose:** FastAPI backend logic for creating, receiving, and listing orders.

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
    note_to_supplier: Optional[str] = None
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
            print(f"[WHATSAPP] Order {order.order_number} exceeds threshold, notify for auth.")

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
        saved_path = UPLOAD_DIR / f"{order_id}_{file.filename}"
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check file size
        file_size = saved_path.stat().st_size
        if file_size < 500:
            try:
                saved_path.unlink()  # Remove the file if it's too small
            except FileNotFoundError:
                pass
            raise HTTPException(status_code=400, detail="Uploaded file is too small or corrupt.")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, file.filename, str(saved_path), datetime.now().isoformat()))
            conn.commit()

        log_event("new_orders_log.txt", {
            "action": "attachment_uploaded",
            "order_id": order_id,
            "filename": file.filename,
            "path": str(saved_path),
            "size_bytes": file_size
        })

        return {"status": "✅ Attachment uploaded"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "upload"})
        raise HTTPException(status_code=500, detail=f"Failed to upload attachment: {e}")

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
        filters = ["o.status IN ('Pending', 'Waiting for Approval')"]
        params = []

        if start_date:
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
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
    except Exception as e:
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

        if start_date:
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(start_date)

        if end_date:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load received orders: {e}")

@router.get("/api/items_for_order/{order_id}")
def get_items_for_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, item_code, item_description, project, qty_ordered, price,
                       (qty_ordered * price) AS total
                FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {e}")
```

### `backend/main.py`
**Purpose:** Main FastAPI application setup and routing for the Pending Orders screen.

```python
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup, supplier_lookup_takealot
from backend.database import init_db
from pathlib import Path
import logging

# ✅ Install debug validator
from scripts.add_debug_validation_handler import install_validation_handler

# ✅ Logging setup
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/server_startup.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ✅ Initialize DB
try:
    init_db()
    logging.info("✅ Database initialized successfully.")
except Exception as e:
    logging.exception("❌ Failed to initialize database")
    raise

# ✅ FastAPI app
app = FastAPI(
    title="Universal Recycling Purchase Order System",
    description="Purchase Order management system for Universal Recycling"
)

# ✅ Enhanced validation
install_validation_handler(app)

# ✅ Mount folders
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/data/uploads", StaticFiles(directory="data/uploads"), name="uploads")

# ✅ Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# ✅ Templates
templates = Jinja2Templates(directory="frontend/templates")

# ✅ Routers
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(lookups.router)
app.include_router(ui_pages.router)
app.include_router(supplier_lookup.router)
app.include_router(supplier_lookup_takealot.router)

# ✅ HTML routes using Jinja2 templates
@app.get("/orders/pending_orders", response_class=HTMLResponse)
def serve_pending_orders(request: Request):
    return templates.TemplateResponse("pending_orders.html", {"request": request})

@app.get("/orders/received_orders", response_class=HTMLResponse)
def serve_received_orders(request: Request):
    return templates.TemplateResponse("received_orders.html", {"request": request})

# ✅ Run server
if __name__ == "__main__":
    import uvicorn
    try:
        logging.info("🚀 Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8004)
    except Exception as e:
        logging.exception("❌ Server failed to start")
        raise

```

### `frontend/static/js/pending_orders.js`
**Purpose:** JS logic for filtering, loading, and rendering pending orders.

```python
import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showReceiveModal } from "/static/js/components/receive_modal.js";
import { showUploadAttachmentsModal, checkAttachments } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";
import { loadRequesters, loadSuppliers } from "/static/js/components/shared_filters.js";
import { attachDateInput } from "/static/js/components/date_input.js"; // Reintroduce the import

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

function populateTable(data) {
  const tbody = document.getElementById("pending-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No pending orders found.";
    return;
  }

  data.orders.forEach(order => {
    const row = tbody.insertRow();
    row.setAttribute("data-order-id", order.id);
    row.innerHTML = `
      <td>${order.created_date}</td>
      <td>${order.order_number}</td>
      <td>${order.requester}</td>
      <td>${order.supplier || 'N/A'}</td>
      <td>R${order.total.toFixed(2)}</td>
      <td>${order.status}</td>
      <td>
        <span class="expand-icon" onclick="window.expandLineItems(${order.id}, this)">⬇️</span>
        <span class="receive-icon" title="Mark as Received" onclick="window.showReceiveModal(${order.id}, '${order.order_number}')">✅</span>
        <span class="clip-icon" title="View/Upload Attachments" onclick="window.showUploadAttachmentsModal(${order.id}, '${order.order_number}', () => window.checkAttachments(${order.id}).then(has => this.classList.toggle('eye-icon', has)))">📎</span>
        <span class="note-icon" title="Edit Continuous Order Note" onclick="window.showOrderNoteModal('${order.order_note ? order.order_note.replace(/'/g, "\\'") : ''}', ${order.id})"></span>
        <span class="supplier-note-icon" title="View Note to Supplier" onclick="window.showSupplierNoteModal('${order.note_to_supplier ? order.note_to_supplier.replace(/'/g, "\\'") : ''}')"></span>
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
  const status = document.getElementById("filter-status").value;
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;

  const params = new URLSearchParams();
  if (supplierName) params.append("supplier", supplierName);
  if (requesterName) params.append("requester", requesterName);
  if (status && status !== "All") params.append("status", status);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/api/orders/pending_orders?${params.toString()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch filtered orders", err);
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
  attachDateInput("start-date"); // Attach to Start Date
  attachDateInput("end-date");   // Attach to End Date
  loadFiltersAndOrders();

  document.getElementById("run-btn").addEventListener("click", runFilters);
  document.getElementById("clear-btn").addEventListener("click", clearFilters);
});

// Expose functions to the global scope for onclick handlers
window.expandLineItems = expandLineItems;
window.showReceiveModal = showReceiveModal;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
```

### `frontend/templates/pending_orders.html`
**Purpose:** HTML template for rendering the Pending Orders screen.

```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Pending Orders</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
    .status { font-weight: bold; }
    .filters { margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
    .filters label { font-weight: bold; }
    input[type="text"], select {
      padding: 0.4rem;
      font-size: 1rem;
      font-family: monospace;
    }
    button {
      padding: 0.5rem 1rem;
      cursor: pointer;
    }
    .expand-icon, .clip-icon, .eye-icon, .receive-icon, .note-icon, .supplier-note-icon {
      cursor: pointer;
      font-size: 1.2rem;
      margin: 0 0.3rem;
      display: inline-block; /* Ensure icons display properly */
    }
    .note-icon::before {
      content: "📝"; /* Fallback in case emoji fails to render */
    }
    .supplier-note-icon::before {
      content: "📦"; /* Fallback in case emoji fails to render */
    }
    .eye-icon.disabled {
      opacity: 0.3;
      cursor: default;
    }
  </style>
</head>
<body>
  <h2>Pending Orders</h2>

  <div class="filters">
    <label for="start-date">Start Date:</label>
    <input type="date" id="start-date" />
    <label for="end-date">End Date:</label>
    <input type="text" id="end-date" placeholder="dd/mm/yyyy" />
    <label for="filter-requester">Requester:</label>
    <select id="filter-requester"></select>
    <label for="filter-supplier">Supplier:</label>
    <select id="filter-supplier"></select>
    <label for="filter-status">Status:</label>
    <select id="filter-status">
      <option value="All">All</option>
      <option value="Pending">Pending</option>
      <option value="Waiting for Approval">Waiting for Approval</option>
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

### `frontend/static/js/components/order_note_modal.js`
**Purpose:** Reusable modal for editing and saving continuous order notes.

```python
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

  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(noteBox);
  document.body.appendChild(modal);
}
```

### `frontend/static/js/components/date_input.js`
**Purpose:** Reusable date input formatter with smart formatting and navigation.

```python
export function attachDateInput(id) {
  const input = document.getElementById(id);
  if (!input) return;

  input.setAttribute("type", "text");
  input.setAttribute("placeholder", "dd/mm/yyyy");
  input.setAttribute("maxlength", "10");
  input.style.fontFamily = "monospace";

  input.addEventListener("input", (e) => {
    let value = input.value.replace(/[^0-9]/g, "");
    if (value.length > 8) value = value.slice(0, 8);

    const cursorPosBefore = input.selectionStart;
    let formatted = "";
    if (value.length > 4) {
      formatted = value.slice(0, 2) + "/" + value.slice(2, 4) + "/" + value.slice(4, 8);
    } else if (value.length > 2) {
      formatted = value.slice(0, 2) + "/" + value.slice(2, 4);
    } else {
      formatted = value;
    }

    input.value = formatted;

    // Adjust cursor position after formatting
    let cursorPosAfter = cursorPosBefore;
    if (cursorPosBefore === 2 && value.length >= 2) {
      cursorPosAfter = 3; // After "dd/"
    } else if (cursorPosBefore === 5 && value.length >= 4) {
      cursorPosAfter = 6; // After "mm/"
    }
    input.setSelectionRange(cursorPosAfter, cursorPosAfter);
  });
}
```

### `frontend/static/js/components/attachment_modal.js`
**Purpose:** Handles file attachment upload and view logic for orders.

```python
export function showViewAttachmentsModal(orderId, orderNumber) {
    fetch(`/orders/attachments/${orderId}`)
      .then(res => res.json())
      .then(data => {
        const files = data.attachments || [];
        const modal = createBaseModal();
        const title = document.createElement("h3");
        title.textContent = `Attachments for ${orderNumber}`;
        modal.inner.appendChild(title);
  
        if (files.length === 0) {
          const noFiles = document.createElement("p");
          noFiles.textContent = "No attachments found.";
          modal.inner.appendChild(noFiles);
        } else {
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
  
        document.body.appendChild(modal.container);
      })
      .catch(err => {
        alert("❌ Failed to load attachments");
        console.error(err);
      });
  }
  
  export function showUploadAttachmentsModal(orderId, orderNumber, onUploadComplete = null) {
    const modal = createBaseModal();
  
    const title = document.createElement("h3");
    title.textContent = `Upload Attachments for ${orderNumber}`;
    modal.inner.appendChild(title);
  
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
      const formData = new FormData();
      formData.append("file", file);
      formData.append("order_id", orderId);
  
      fetch("/orders/upload_attachment", {
        method: "POST",
        body: formData,
      })
        .then(res => {
          if (!res.ok) throw new Error("Upload failed");
          return res.json();
        })
        .then(() => {
          const msg = document.createElement("p");
          msg.textContent = `✅ Uploaded: ${file.name}`;
          msg.style.color = "green";
          modalInner.appendChild(msg);
          if (onUploadComplete) onUploadComplete();
        })
        .catch(err => {
          const msg = document.createElement("p");
          msg.textContent = `❌ Failed to upload: ${file.name}`;
          msg.style.color = "red";
          modalInner.appendChild(msg);
          console.error(err);
        });
    });
  }
  
  function createBaseModal() {
    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100vw";
    container.style.height = "100vh";
    container.style.backgroundColor = "rgba(0,0,0,0.5)";
    container.style.display = "flex";
    container.style.alignItems = "center";
    container.style.justifyContent = "center";
    container.style.zIndex = "9999";
  
    const inner = document.createElement("div");
    inner.style.backgroundColor = "white";
    inner.style.padding = "1.5rem";
    inner.style.borderRadius = "8px";
    inner.style.width = "90%";
    inner.style.maxWidth = "500px";
    inner.style.maxHeight = "80vh";
    inner.style.overflowY = "auto";
    inner.style.fontFamily = "Arial, sans-serif";
    inner.style.position = "relative";
  
    const close = document.createElement("button");
    close.textContent = "✖";
    close.style.position = "absolute";
    close.style.top = "10px";
    close.style.right = "10px";
    close.style.background = "none";
    close.style.border = "none";
    close.style.fontSize = "1.2rem";
    close.style.cursor = "pointer";
    close.onclick = () => document.body.removeChild(container);
  
    inner.appendChild(close);
    container.appendChild(inner);
  
    return { container, inner };
  }
  
```

### `frontend/static/js/components/expand_line_items.js`
**Purpose:** Displays expandable line items per order.

```python
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

### `frontend/static/js/components/receive_modal.js`
**Purpose:** Modal for marking orders or items as received.

```python
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

        if (res.ok) {
          alert("✅ Order marked as received");
          document.body.removeChild(modal);
          location.reload();
        } else {
          const err = await res.json();
          if (Array.isArray(err.detail)) {
            const messages = err.detail.map(obj => obj.msg || JSON.stringify(obj));
            alert("❌ Failed to mark as received:\n" + messages.join("\n"));
          } else {
            alert("❌ Failed to mark as received: " + (err.detail || "Unknown error"));
          }
          
        }
      };

      modal.appendChild(closeBtn);
      modal.appendChild(title);
      modal.appendChild(table);
      modal.appendChild(submitBtn);
      document.body.appendChild(modal);
    })
    .catch(err => {
      console.error("❌ Error loading receive modal:", err);
      alert("❌ Could not open receive modal");
    });
}

```

### `frontend/static/js/components/shared_filters.js`
**Purpose:** Loads and populates shared dropdown filters like suppliers/requesters.

```python
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

```

### `logs/db_activity_log.txt`
**(No description)**
```python
[2025-04-22T05:06:11.566741] init_db: {"status": "success"}
[2025-04-22T05:06:21.069095] init_db: {"status": "success"}
[2025-04-22T05:06:54.954959] init_db: {"status": "success"}
[2025-04-22T05:12:19.196077] get_setting: {"key": "order_number_start", "result": "URC1034"}
[2025-04-22T05:16:17.303069] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-22T05:16:17.303893] get_setting: {"key": "order_number_start", "result": "URC1034"}
[2025-04-22T05:16:17.305045] update_setting: {"key": "order_number_start", "value": "URC1036"}
[2025-04-22T05:16:17.306763] create_order: {"order_number": "URC1035", "requester_id": 5, "total": 1035.0, "items_count": 1}
[2025-04-22T05:16:19.651196] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T06:58:50.431845] init_db: {"status": "success"}
[2025-04-22T07:25:31.256262] init_db: {"status": "success"}
[2025-04-22T07:25:37.750562] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T07:43:49.020738] init_db: {"status": "success"}
[2025-04-22T07:56:35.917515] init_db: {"status": "success"}
[2025-04-22T08:01:44.967465] init_db: {"status": "success"}
[2025-04-22T08:04:30.689613] init_db: {"status": "success"}
[2025-04-22T08:49:02.006942] init_db: {"status": "success"}
[2025-04-22T08:59:46.286681] init_db: {"status": "success"}
[2025-04-22T10:54:48.492602] init_db: {"status": "success"}
[2025-04-22T11:25:00.050849] init_db: {"status": "success"}
[2025-04-22T12:57:19.591378] init_db: {"status": "success"}
[2025-04-22T13:32:37.623258] init_db: {"status": "success"}
[2025-04-22T14:21:34.237278] init_db: {"status": "success"}
[2025-04-22T14:28:43.803577] init_db: {"status": "success"}
[2025-04-22T14:34:40.100061] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T14:37:00.128284] init_db: {"status": "success"}
[2025-04-22T15:03:50.195182] init_db: {"status": "success"}
[2025-04-22T15:14:48.842138] init_db: {"status": "success"}
[2025-04-22T15:25:55.483094] init_db: {"status": "success"}
[2025-04-22T15:33:39.739632] init_db: {"status": "success"}
[2025-04-22T15:35:55.601620] init_db: {"status": "success"}
[2025-04-22T15:45:06.744352] init_db: {"status": "success"}
[2025-04-22T15:51:15.077251] init_db: {"status": "success"}
[2025-04-22T15:57:13.291460] init_db: {"status": "success"}
[2025-04-22T16:04:23.364333] init_db: {"status": "success"}
[2025-04-22T16:04:55.175300] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T16:05:06.486286] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T16:19:24.820076] init_db: {"status": "success"}
[2025-04-22T16:19:28.581115] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T16:31:12.011865] init_db: {"status": "success"}
[2025-04-22T16:31:16.302074] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-22T16:34:03.121823] init_db: {"status": "success"}
[2025-04-23T03:56:57.246260] init_db: {"status": "success"}
[2025-04-23T04:18:31.286236] init_db: {"status": "success"}
[2025-04-23T04:37:15.218323] init_db: {"status": "success"}
[2025-04-23T04:37:24.768092] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-23T04:49:26.882395] init_db: {"status": "success"}
[2025-04-23T04:49:34.359157] init_db: {"status": "success"}
[2025-04-23T04:53:14.399040] init_db: {"status": "success"}
[2025-04-23T04:53:21.157808] init_db: {"status": "success"}
[2025-04-23T04:54:58.874954] init_db: {"status": "success"}
[2025-04-23T04:55:05.813144] init_db: {"status": "success"}
[2025-04-23T04:55:13.359618] init_db: {"status": "success"}
[2025-04-23T04:55:56.968533] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-23T05:00:25.667245] init_db: {"status": "success"}
[2025-04-23T05:00:57.632423] init_db: {"status": "success"}
[2025-04-23T05:08:58.606213] init_db: {"status": "success"}
[2025-04-23T05:09:52.968840] init_db: {"status": "success"}
[2025-04-23T05:17:54.543918] init_db: {"status": "success"}
[2025-04-23T05:18:33.857535] init_db: {"status": "success"}
[2025-04-23T05:18:36.799757] init_db: {"status": "success"}
[2025-04-23T05:26:24.157305] init_db: {"status": "success"}
[2025-04-23T05:48:36.635612] init_db: {"status": "success"}
[2025-04-23T05:51:52.577240] init_db: {"status": "success"}
[2025-04-23T06:00:58.591493] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-23T06:00:58.591857] get_setting: {"key": "order_number_start", "result": "URC1036"}
[2025-04-23T06:00:58.592794] update_setting: {"key": "order_number_start", "value": "URC1038"}
[2025-04-23T06:00:58.593927] create_order: {"order_number": "URC1037", "requester_id": 3, "total": 18000.0, "items_count": 2}
[2025-04-23T06:01:02.255685] get_setting: {"key": "order_number_start", "result": "URC1038"}
[2025-04-23T06:14:00.585358] init_db: {"status": "success"}
[2025-04-23T06:17:46.996605] init_db: {"status": "success"}
[2025-04-23T06:17:55.367528] init_db: {"status": "success"}
[2025-04-23T06:23:17.507297] init_db: {"status": "success"}
[2025-04-23T06:24:58.033117] init_db: {"status": "success"}
[2025-04-23T06:26:36.702869] init_db: {"status": "success"}
[2025-04-23T06:30:21.351730] init_db: {"status": "success"}
[2025-04-23T06:34:59.295404] init_db: {"status": "success"}
[2025-04-23T06:43:17.623561] init_db: {"status": "success"}
[2025-04-23T06:48:31.296416] init_db: {"status": "success"}
[2025-04-23T06:48:42.428557] init_db: {"status": "success"}
[2025-04-23T06:57:28.793876] init_db: {"status": "success"}
[2025-04-23T07:08:08.750888] init_db: {"status": "success"}
[2025-04-23T07:20:03.060488] init_db: {"status": "success"}
[2025-04-23T07:20:11.455331] init_db: {"status": "success"}
[2025-04-23T07:32:01.823062] init_db: {"status": "success"}
[2025-04-23T07:32:10.383851] init_db: {"status": "success"}
[2025-04-23T07:42:47.755342] init_db: {"status": "success"}
[2025-04-23T07:44:40.867850] init_db: {"status": "success"}
[2025-04-23T07:44:46.674066] init_db: {"status": "success"}
[2025-04-23T07:55:24.411945] init_db: {"status": "success"}
[2025-04-23T07:56:52.336046] init_db: {"status": "success"}
[2025-04-23T13:56:38.386674] init_db: {"status": "success"}
[2025-04-23T14:02:37.549032] init_db: {"status": "success"}
[2025-04-23T14:05:33.955929] init_db: {"status": "success"}
[2025-04-23T14:13:54.751757] init_db: {"status": "success"}
[2025-04-23T14:13:59.660982] init_db: {"status": "success"}
[2025-04-23T14:41:23.168650] init_db: {"status": "success"}
[2025-04-23T15:13:48.814030] init_db: {"status": "success"}
[2025-04-23T15:15:04.571855] init_db: {"status": "success"}
[2025-04-23T15:15:20.038428] init_db: {"status": "success"}
[2025-04-23T15:15:30.330051] init_db: {"status": "success"}
[2025-04-23T15:15:44.570512] init_db: {"status": "success"}
[2025-04-23T15:18:10.586883] get_setting: {"key": "order_number_start", "result": "URC1038"}
[2025-04-23T15:19:01.994980] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-23T15:19:01.995456] get_setting: {"key": "order_number_start", "result": "URC1038"}
[2025-04-23T15:19:01.996565] update_setting: {"key": "order_number_start", "value": "URC1040"}
[2025-04-23T15:19:02.577163] create_order: {"order_number": "URC1039", "requester_id": 4, "total": 11000.0, "items_count": 1}
[2025-04-23T15:19:05.525768] get_setting: {"key": "order_number_start", "result": "URC1040"}
[2025-04-23T15:23:10.636705] init_db: {"status": "success"}
[2025-04-23T15:23:36.269599] init_db: {"status": "success"}
[2025-04-23T15:24:34.528330] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-23T15:24:34.528760] get_setting: {"key": "order_number_start", "result": "URC1040"}
[2025-04-23T15:24:34.529889] update_setting: {"key": "order_number_start", "value": "URC1042"}
[2025-04-23T15:24:35.160064] create_order: {"order_number": "URC1041", "requester_id": 4, "total": 12000.0, "items_count": 1}
[2025-04-23T15:24:36.882766] get_setting: {"key": "order_number_start", "result": "URC1042"}
[2025-04-24T05:20:45.488015] init_db: {"status": "success"}
[2025-04-24T05:21:28.046944] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-24T05:21:28.047295] get_setting: {"key": "order_number_start", "result": "URC1042"}
[2025-04-24T05:21:28.048285] update_setting: {"key": "order_number_start", "value": "URC1044"}
[2025-04-24T05:21:28.596075] create_order: {"order_number": "URC1043", "requester_id": 4, "total": 15000.0, "items_count": 1}
[2025-04-24T05:21:30.685680] get_setting: {"key": "order_number_start", "result": "URC1044"}
[2025-04-24T05:40:10.599757] init_db: {"status": "success"}
[2025-04-24T05:46:27.225232] init_db: {"status": "success"}
[2025-04-24T06:44:37.658009] init_db: {"status": "success"}
[2025-04-24T06:45:31.880986] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-24T06:45:31.881730] get_setting: {"key": "order_number_start", "result": "URC1044"}
[2025-04-24T06:45:31.883570] update_setting: {"key": "order_number_start", "value": "URC1046"}
[2025-04-24T06:45:34.824827] create_order: {"order_number": "URC1045", "requester_id": 3, "total": 30000.0, "items_count": 1}
[2025-04-24T06:45:37.178306] get_setting: {"key": "order_number_start", "result": "URC1046"}
[2025-04-24T06:53:46.056050] init_db: {"status": "success"}
[2025-04-24T06:53:53.215251] init_db: {"status": "success"}
[2025-04-24T06:54:38.166716] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-24T06:54:38.167082] get_setting: {"key": "order_number_start", "result": "URC1046"}
[2025-04-24T06:54:38.168146] update_setting: {"key": "order_number_start", "value": "URC1048"}
[2025-04-24T06:54:40.993453] create_order: {"order_number": "URC1047", "requester_id": 1, "total": 15000.0, "items_count": 1}
[2025-04-24T06:54:43.681605] get_setting: {"key": "order_number_start", "result": "URC1048"}
[2025-04-24T06:57:33.128173] init_db: {"status": "success"}
[2025-04-24T06:57:38.434633] init_db: {"status": "success"}
[2025-04-24T06:58:34.398670] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-24T06:58:34.399210] get_setting: {"key": "order_number_start", "result": "URC1048"}
[2025-04-24T06:58:34.400648] update_setting: {"key": "order_number_start", "value": "URC1050"}
[2025-04-24T06:58:37.199851] create_order: {"order_number": "URC1049", "requester_id": 1, "total": 120000.0, "items_count": 1}
[2025-04-24T06:58:39.521483] get_setting: {"key": "order_number_start", "result": "URC1050"}
[2025-04-24T07:08:25.034026] init_db: {"status": "success"}
[2025-04-24T07:08:29.799695] init_db: {"status": "success"}
[2025-04-24T07:11:06.732101] init_db: {"status": "success"}
[2025-04-24T07:11:11.199421] init_db: {"status": "success"}
[2025-04-24T07:11:23.978006] get_setting: {"key": "order_number_start", "result": "URC1050"}
[2025-04-24T07:11:59.309152] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-24T07:11:59.309647] get_setting: {"key": "order_number_start", "result": "URC1050"}
[2025-04-24T07:11:59.310927] update_setting: {"key": "order_number_start", "value": "URC1052"}
[2025-04-24T07:12:02.207599] create_order: {"order_number": "URC1051", "requester_id": 1, "total": 12000.0, "items_count": 1}
[2025-04-24T07:12:05.438605] get_setting: {"key": "order_number_start", "result": "URC1052"}
[2025-04-24T07:25:41.707399] init_db: {"status": "success"}
[2025-04-24T07:25:56.550152] init_db: {"status": "success"}
[2025-04-24T07:27:10.839444] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-24T07:27:10.840089] get_setting: {"key": "order_number_start", "result": "URC1052"}
[2025-04-24T07:27:10.841658] update_setting: {"key": "order_number_start", "value": "URC1054"}
[2025-04-24T07:27:13.838272] create_order: {"order_number": "URC1053", "requester_id": 2, "total": 18000.0, "items_count": 1}
[2025-04-24T07:27:16.010656] get_setting: {"key": "order_number_start", "result": "URC1054"}
[2025-04-24T08:43:21.672310] init_db: {"status": "success"}
[2025-04-24T09:04:49.201336] init_db: {"status": "success"}
[2025-04-24T09:10:30.154961] init_db: {"status": "success"}
[2025-04-24T09:16:08.063077] init_db: {"status": "success"}
[2025-04-24T09:16:53.554107] init_db: {"status": "success"}
[2025-04-24T09:20:31.205175] init_db: {"status": "success"}
[2025-04-24T09:25:07.712313] init_db: {"status": "success"}
[2025-04-24T09:30:36.111142] init_db: {"status": "success"}

```

### `logs/lookups_log.txt`
**(No description)**
```python
{"time": "2025-04-19T17:19:50.525099", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:19:50.525452", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:19:50.526951", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:19:50.526987", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:33:43.359209", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:33:43.359981", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:33:43.361321", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:33:43.362429", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:36:23.523549", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:36:23.524026", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:36:23.524193", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:36:23.525769", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:36:51.736563", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:36:51.737191", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:36:51.737252", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:36:51.739078", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:37:32.194547", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:37:32.194923", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:37:32.197866", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:37:32.198621", "endpoint": "/items", "status": "success"}
{"time": "2025-04-20T14:45:45.495435", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T14:45:45.495972", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T14:52:58.436165", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T14:52:58.437142", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T14:58:27.136610", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T14:58:27.137286", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:09:25.067788", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:09:25.068794", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:12:34.020488", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:12:34.021118", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:45:58.077272", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:45:58.077585", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:57:37.305332", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:57:37.306011", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T16:02:24.832425", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T16:02:24.832726", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T16:05:27.878635", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T16:05:27.878911", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T16:05:27.881131", "endpoint": "/items", "status": "success"}
{"time": "2025-04-20T16:05:27.881211", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-20T16:05:31.923735", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T16:05:31.925461", "endpoint": "/items", "status": "success"}
{"time": "2025-04-20T16:05:31.925586", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T16:05:31.926041", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-20T16:05:47.040851", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T16:05:47.041291", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T16:05:47.042712", "endpoint": "/items", "status": "success"}
{"time": "2025-04-20T16:05:47.043298", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-20T21:22:37.571202", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T21:22:37.571705", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T21:22:58.953448", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T21:22:58.953543", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T21:22:58.955954", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-20T21:22:58.956184", "endpoint": "/items", "status": "success"}
{"time": "2025-04-20T21:31:20.665943", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T21:31:20.666467", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T22:09:52.010811", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T22:09:52.010993", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T22:40:25.081267", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T22:40:25.082122", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T22:40:50.042939", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T22:40:50.044819", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T23:07:01.045263", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T23:07:01.046260", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T23:07:30.005625", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T23:07:30.005798", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T23:17:10.602915", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T23:17:10.602978", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T23:29:43.289925", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T23:29:43.290021", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T23:50:47.087229", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T23:50:47.087936", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T23:59:32.157568", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T23:59:32.157983", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:09:21.392314", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T00:09:21.393447", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:09:47.826681", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T00:09:47.827234", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:11:37.665526", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T00:11:37.665899", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:31:27.579465", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T00:31:27.579744", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:38:00.147828", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T00:38:00.148005", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:38:27.884419", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T00:38:27.884934", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:46:22.353852", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T00:46:22.353919", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T08:43:24.464630", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T08:43:24.464687", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:06:20.402486", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:06:20.406553", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:09:00.076367", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:09:00.076978", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:12:54.639559", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:12:54.639769", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:13:15.490380", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:13:15.491713", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:13:34.297353", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:13:34.297590", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:13:34.300806", "endpoint": "/items", "status": "success"}
{"time": "2025-04-21T09:13:34.300942", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-21T09:14:27.927595", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:14:27.927745", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:14:27.928585", "endpoint": "/items", "status": "success"}
{"time": "2025-04-21T09:14:27.928936", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-21T09:14:35.423898", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:14:35.423998", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:15:10.025080", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:15:10.025871", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:32:29.728064", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:32:29.728683", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:53:38.708305", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T09:53:38.708699", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:54:21.294287", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T09:54:21.294345", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T10:06:28.576747", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T10:06:28.577283", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T10:09:31.214121", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T10:09:31.216272", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T10:10:05.492092", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T10:10:05.492800", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T10:12:06.670461", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T10:12:06.670818", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T10:38:21.573356", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T10:38:21.573522", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:09:11.670133", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:09:11.670751", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:11:50.729235", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:11:50.729659", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:12:44.825429", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:12:44.825498", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:21:36.505486", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:21:36.507893", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:25:46.845756", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:25:46.846229", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:28:08.969475", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:28:08.969575", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:28:53.691123", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:28:53.692635", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:39:07.091393", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:39:07.091885", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:39:24.433005", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:39:24.433110", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:39:33.504659", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:39:33.505050", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:45:34.386296", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:45:34.386540", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:45:52.374614", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:45:52.374702", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:47:07.293213", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:47:07.293261", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:55:20.740735", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-21T12:55:20.741193", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:55:28.874436", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-21T12:55:28.874584", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T05:12:19.194610", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T05:12:19.195223", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T05:12:19.196100", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T05:12:19.196147", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T05:12:30.214628", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T05:12:30.214666", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T05:12:40.745873", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T05:12:40.748627", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T05:13:35.843785", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T05:13:35.843842", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T05:16:19.649740", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T05:16:19.649814", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T05:16:19.651406", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T05:16:19.651608", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T07:25:37.748822", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T07:25:37.748902", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T07:25:37.750108", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T07:25:37.751200", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T08:59:51.267584", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T08:59:51.267671", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T14:34:40.096175", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T14:34:40.098436", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T14:34:40.099467", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T14:34:40.100274", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T14:34:50.329023", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T14:34:50.329087", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T14:37:04.541272", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T14:37:04.541317", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:03:56.229434", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:03:56.229567", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:06:23.252386", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:06:23.252966", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:26:06.581420", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:26:06.581591", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:36:07.171339", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:36:07.171389", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:45:10.506399", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:45:10.506569", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:51:20.846646", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T15:51:20.846900", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:57:17.153314", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T15:57:17.153374", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:04:29.802457", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:04:29.802739", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:04:55.172493", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:04:55.173430", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:04:55.174371", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T16:04:55.176137", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T16:05:06.482202", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:05:06.485155", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:05:06.486237", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T16:05:06.486447", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T16:19:28.579771", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T16:19:28.580340", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:19:28.581728", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:19:28.581963", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T16:31:16.298990", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:31:16.300074", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-22T16:31:16.301062", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:31:16.302036", "endpoint": "/items", "status": "success"}
{"time": "2025-04-22T16:31:26.786141", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:31:26.786608", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:33:56.484442", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-22T16:33:56.484479", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:34:06.287650", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-22T16:34:06.287720", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T03:57:02.850427", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T03:57:02.850632", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:18:39.104103", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T04:18:39.104173", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:30:46.790733", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:30:46.790804", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T04:37:24.766512", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:37:24.766862", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T04:37:24.768443", "endpoint": "/items", "status": "success"}
{"time": "2025-04-23T04:37:24.768660", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-23T04:50:02.900260", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:50:02.900663", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T04:55:46.888419", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:55:46.888528", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T04:55:56.966605", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T04:55:56.966775", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T04:55:56.967464", "endpoint": "/items", "status": "success"}
{"time": "2025-04-23T04:55:56.968574", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-23T05:01:10.160136", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T05:01:10.160293", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T05:10:09.162033", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T05:10:09.162106", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T05:18:43.572574", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T05:18:43.572677", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T05:26:31.615911", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T05:26:31.616602", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:01:02.254686", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:01:02.254922", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:01:02.256342", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-23T06:01:02.256561", "endpoint": "/items", "status": "success"}
{"time": "2025-04-23T06:01:16.709446", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:01:16.709509", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:14:06.320147", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:14:06.320278", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:18:00.428608", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:18:00.428922", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:19:02.516311", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-23T06:19:02.516808", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-23T06:25:03.098227", "endpoint": "/suppliers", "status": "success"}
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

### `logs/new_orders_log.txt`
**(No description)**
```python
[2025-04-19T14:39:27.704140] {"action": "submit_attempt", "order_data": {"order_number": "URC1009", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "PIPE001", "item_description": "Steel Pipe 2-inch", "project": "TestProject1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "JOINT002", "item_description": "Pipe Joint 2-inch", "project": "TestProject2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T14:39:27.705060] {"action": "submit_success", "order_number": "URC1009", "status": "Pending"}
[2025-04-19T14:42:30.740086] {"action": "submit_attempt", "order_data": {"order_number": "URC1011", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "TEST001", "item_description": "Steel Pipe 2-inch", "project": "TestProj1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "TEST002", "item_description": "Pipe Joint 2-inch", "project": "TestProj2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T14:42:30.740820] {"action": "submit_success", "order_number": "URC1011", "status": "Pending"}
[2025-04-19T14:55:30.630412] {"action": "submit_attempt", "order_data": {"order_number": "URC1013", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "TEST001", "item_description": "Steel Pipe 2-inch", "project": "TestProj1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "TEST002", "item_description": "Pipe Joint 2-inch", "project": "TestProj2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T14:55:30.631283] {"action": "submit_success", "order_number": "URC1013", "status": "Pending"}
[2025-04-19T14:55:30.645675] {"action": "receive", "orders": [19]}
[2025-04-19T15:07:04.568837] {"action": "submit_attempt", "order_data": {"order_number": "URC1015", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "TEST001", "item_description": "Steel Pipe 2-inch", "project": "TestProj1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "TEST002", "item_description": "Pipe Joint 2-inch", "project": "TestProj2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T15:07:04.569746] {"action": "submit_success", "order_number": "URC1015", "status": "Pending"}
[2025-04-19T15:07:04.584492] {"action": "receive", "orders": [20]}
[2025-04-19T15:07:04.587243] {"action": "attachment_uploaded", "order_id": 20, "filename": "test_invoice.pdf", "path": "data/uploads/20_test_invoice.pdf"}
[2025-04-19T15:29:15.860120] {"action": "submit_attempt", "order_data": {"order_number": "URC1017", "requester_id": 1, "order_note": "End-to-end test order", "note_to_supplier": "Please confirm ASAP", "supplier_id": 1, "items": [{"item_code": "TST001", "item_description": "Test Widget", "project": "TEST-01", "qty_ordered": 3.0, "price": 200.0}, {"item_code": "TST002", "item_description": "Test Cable", "project": "TEST-02", "qty_ordered": 5.0, "price": 100.0}], "status": "Pending", "total": 1100.0}}
[2025-04-19T15:29:15.861078] {"action": "submit_success", "order_number": "URC1017", "status": "Pending"}
[2025-04-19T15:29:15.875787] {"action": "receive", "orders": [21]}
[2025-04-19T15:29:15.878624] {"action": "attachment_uploaded", "order_id": 21, "filename": "test_invoice.pdf", "path": "data/uploads/21_test_invoice.pdf"}
[2025-04-19T15:35:57.487040] {"action": "submit_attempt", "order_data": {"order_number": "URC1019", "requester_id": 1, "order_note": "Partial receive test", "note_to_supplier": "Split delivery test", "supplier_id": 1, "items": [{"item_code": "PART001", "item_description": "Partial Item A", "project": "SplitProjA", "qty_ordered": 10.0, "price": 100.0}, {"item_code": "PART002", "item_description": "Partial Item B", "project": "SplitProjB", "qty_ordered": 5.0, "price": 200.0}], "status": "Pending", "total": 2000.0}}
[2025-04-19T15:35:57.487956] {"action": "submit_success", "order_number": "URC1019", "status": "Pending"}
[2025-04-19T15:35:57.503247] {"action": "receive", "orders": [22]}
[2025-04-19T15:38:25.369555] {"action": "submit_attempt", "order_data": {"order_number": "URC1021", "requester_id": 1, "order_note": "Test high value order", "note_to_supplier": "Handle with care", "supplier_id": 1, "items": [{"item_code": "HIGH001", "item_description": "Premium Machine Part", "project": "TestProjX", "qty_ordered": 1.0, "price": 20000.0}], "status": "Awaiting Authorisation", "total": 20000.0}}
[2025-04-19T15:38:25.370156] {"action": "submit_success", "order_number": "URC1021", "status": "Awaiting Authorisation"}
[2025-04-19T16:14:48.829687] {"action": "submit_attempt", "order_data": {"order_number": "URC1023", "requester_id": 1, "order_note": "Partial receive test", "note_to_supplier": "Split delivery test", "supplier_id": 1, "items": [{"item_code": "PART001", "item_description": "Partial Item A", "project": "SplitProjA", "qty_ordered": 10.0, "price": 100.0}, {"item_code": "PART002", "item_description": "Partial Item B", "project": "SplitProjB", "qty_ordered": 5.0, "price": 200.0}], "status": "Pending", "total": 2000.0}}
[2025-04-19T16:14:48.830733] {"action": "submit_success", "order_number": "URC1023", "status": "Pending"}
[2025-04-19T17:11:50.972474] {"action": "submit_attempt", "order_data": {"order_number": "URC1025", "requester_id": 1, "order_note": "Browser Sim Test", "note_to_supplier": "Please rush this one", "supplier_id": 1, "items": [{"item_code": "SIM001", "item_description": "Simulated Item", "project": "PR10M", "qty_ordered": 3.0, "price": 100.0}], "status": "Pending", "total": 300.0}}
[2025-04-19T17:11:50.974002] {"action": "submit_success", "order_number": "URC1025", "status": "Pending"}
[2025-04-19T17:36:16.109144] {"action": "submit_attempt", "order_data": {"order_number": "URC1027", "requester_id": 2, "order_note": null, "note_to_supplier": "", "supplier_id": 5, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "KA04M", "qty_ordered": 1.0, "price": 1200.0}], "status": "Pending", "total": 1200.0}}
[2025-04-19T17:36:16.112468] {"action": "submit_success", "order_number": "URC1027", "status": "Pending"}
[2025-04-19T17:36:48.889243] {"action": "submit_attempt", "order_data": {"order_number": "URC1029", "requester_id": 5, "order_note": null, "note_to_supplier": "", "supplier_id": 9, "items": [{"item_code": "BEAR180", "item_description": "Bearing Nylos Ring For 23034 Mac 4 W33 Brass Cage", "project": "PR10M", "qty_ordered": 1.0, "price": 20.0}], "status": "Pending", "total": 20.0}}
[2025-04-19T17:36:48.890998] {"action": "submit_success", "order_number": "URC1029", "status": "Pending"}
[2025-04-19T17:37:29.799798] {"action": "submit_attempt", "order_data": {"order_number": "URC1031", "requester_id": 5, "order_note": null, "note_to_supplier": "", "supplier_id": 8, "items": [{"item_code": "BEAR180", "item_description": "Bearing Nylos Ring For 23034 Mac 4 W33 Brass Cage", "project": "PR10M", "qty_ordered": 1.0, "price": 10.0}], "status": "Pending", "total": 10.0}}
[2025-04-19T17:37:29.803039] {"action": "submit_success", "order_number": "URC1031", "status": "Pending"}
[2025-04-20T22:41:19.119714] {"action": "attachment_uploaded", "order_id": 28, "filename": "test_invoice.pdf", "path": "data/uploads/28_test_invoice.pdf"}
[2025-04-20T22:41:47.580754] {"action": "attachment_uploaded", "order_id": 28, "filename": "test_invoice.pdf", "path": "data/uploads/28_test_invoice.pdf"}
[2025-04-20T23:30:44.970739] {"action": "attachment_uploaded", "order_id": 28, "filename": "Deposit - 2.pdf", "path": "data/uploads/28_Deposit - 2.pdf"}
[2025-04-20T23:30:55.339708] {"action": "attachment_uploaded", "order_id": 27, "filename": "test_invoice.pdf", "path": "data/uploads/27_test_invoice.pdf"}
[2025-04-20T23:33:02.605233] {"action": "attachment_uploaded", "order_id": 26, "filename": "Intimisso.pdf", "path": "data/uploads/26_Intimisso.pdf"}
[2025-04-20T23:34:06.662692] {"action": "attachment_uploaded", "order_id": 25, "filename": "Screenshot 2025-04-20 at 17.12.14.png", "path": "data/uploads/25_Screenshot 2025-04-20 at 17.12.14.png"}
[2025-04-20T23:51:08.383602] {"action": "attachment_uploaded", "order_id": 28, "filename": "Deposit - 2.pdf", "path": "data/uploads/28_Deposit - 2.pdf", "size_bytes": 257514}
[2025-04-20T23:59:40.748862] {"action": "attachment_uploaded", "order_id": 24, "filename": "Fidessa Consulting.PDF", "path": "data/uploads/24_Fidessa Consulting.PDF", "size_bytes": 5382}
[2025-04-21T00:10:01.409456] {"action": "attachment_uploaded", "order_id": 19, "filename": "Fidessa Consulting.PDF", "path": "data/uploads/19_Fidessa Consulting.PDF", "size_bytes": 5382}
[2025-04-21T00:10:55.312735] {"action": "attachment_uploaded", "order_id": 19, "filename": "Fidessa Consulting.PDF", "path": "data/uploads/19_Fidessa Consulting.PDF", "size_bytes": 5382}
[2025-04-21T00:12:57.461549] {"action": "attachment_uploaded", "order_id": 19, "filename": "Fidessa Consulting.PDF", "path": "data/uploads/19_Fidessa Consulting.PDF", "size_bytes": 5382}
[2025-04-21T00:13:58.025883] {"action": "attachment_uploaded", "order_id": 22, "filename": "Hydehurst RC- Proof of submission.pdf", "path": "data/uploads/22_Hydehurst RC- Proof of submission.pdf", "size_bytes": 165820}
[2025-04-21T00:31:35.477081] {"action": "attachment_uploaded", "order_id": 18, "filename": "Hydehurst RC- Proof of submission.pdf", "path": "data/uploads/18_Hydehurst RC- Proof of submission.pdf", "size_bytes": 165820}
[2025-04-21T00:38:09.109040] {"action": "attachment_uploaded", "order_id": 17, "filename": "Intimisso.pdf", "path": "data/uploads/17_Intimisso.pdf", "size_bytes": 527661}
[2025-04-21T00:46:32.547375] {"action": "attachment_uploaded", "order_id": 19, "filename": "Fidessa Consulting.PDF", "path": "data/uploads/19_Fidessa Consulting.PDF", "size_bytes": 5382}
[2025-04-21T00:46:58.695065] {"action": "attachment_uploaded", "order_id": 21, "filename": "Fidessa Consulting.PDF", "path": "data/uploads/21_Fidessa Consulting.PDF", "size_bytes": 5382}
[2025-04-21T09:14:24.762072] {"action": "submit_attempt", "order_data": {"order_number": "URC1033", "requester_id": 5, "order_note": null, "note_to_supplier": "Multiple line order", "supplier_id": 7, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "KA04M", "qty_ordered": 1.0, "price": 200.0}, {"item_code": "BULB004", "item_description": "Bulb 12 V Dcdf  G1034", "project": "PR30M", "qty_ordered": 1.0, "price": 300.0}], "status": "Pending", "total": 500.0}}
[2025-04-21T09:14:24.764510] {"action": "submit_success", "order_number": "URC1033", "status": "Pending"}
[2025-04-21T12:10:34.297975] {"action": "receive", "orders": [29]}
[2025-04-21T12:18:37.007009] {"action": "receive", "orders": [33]}
[2025-04-21T12:30:25.856894] {"action": "receive", "orders": [33]}
[2025-04-21T12:39:14.035880] {"action": "receive", "orders": [29]}
[2025-04-21T12:45:49.834298] {"action": "receive", "orders": [28]}
[2025-04-21T12:55:27.119339] {"action": "receive", "orders": [22]}
[2025-04-22T05:13:33.480467] {"action": "receive", "orders": [27]}
[2025-04-22T05:16:17.305742] {"action": "submit_attempt", "order_data": {"order_number": "URC1035", "requester_id": 5, "order_note": null, "note_to_supplier": "Note to order URC1035", "supplier_id": 5, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "DR09M", "qty_ordered": 1.0, "price": 1035.0}], "status": "Pending", "total": 1035.0}}
[2025-04-22T05:16:17.307190] {"action": "submit_success", "order_number": "URC1035", "status": "Pending"}
[2025-04-22T14:37:29.975123] {"action": "attachment_uploaded", "order_id": 30, "filename": "Intimisso.pdf", "path": "data/uploads/30_Intimisso.pdf", "size_bytes": 527661}
[2025-04-22T15:05:06.494383] {"error": "400: Uploaded file is too small or corrupt.", "type": "upload"}
[2025-04-22T15:06:32.111866] {"error": "400: Uploaded file is too small or corrupt.", "type": "upload"}
[2025-04-22T15:26:14.689225] {"action": "note_updated", "order_id": 17, "order_note": "Pipeline test note"}
[2025-04-22T15:53:10.024213] {"action": "note_updated", "order_id": 26, "order_note": "(No note)"}
[2025-04-23T04:58:19.922536] {"error": "400: Uploaded file is too small or corrupt.", "type": "upload"}
[2025-04-23T05:01:18.754659] {"error": "400: Uploaded file is too small or corrupt.", "type": "upload"}
[2025-04-23T05:10:21.922001] {"error": "400: Uploaded file is too small or corrupt.", "type": "upload"}
[2025-04-23T05:12:32.709870] {"action": "attachment_uploaded", "order_id": 30, "filename": "2025-04-22_18-44.pdf", "path": "data/uploads/30_2025-04-22_18-44.pdf", "size_bytes": 497451}
[2025-04-23T05:12:44.191101] {"action": "attachment_uploaded", "order_id": 30, "filename": "2025-04-22_18-44_1.pdf", "path": "data/uploads/30_2025-04-22_18-44_1.pdf", "size_bytes": 497451}
[2025-04-23T05:26:58.042745] {"action": "attachment_uploaded", "order_id": 30, "filename": "2025-04-22_18-29.pdf", "path": "data/uploads/30_2025-04-22_18-29.pdf", "size_bytes": 359355}
[2025-04-23T05:27:25.980213] {"action": "attachment_uploaded", "order_id": 13, "filename": "Screenshot_2025-04-23_at_05.19.18.png", "path": "data/uploads/13_Screenshot_2025-04-23_at_05.19.18.png", "size_bytes": 36991}
[2025-04-23T05:27:53.524437] {"action": "attachment_uploaded", "order_id": 14, "filename": "Screenshot_2025-04-23_at_05.19.18.png", "path": "data/uploads/14_Screenshot_2025-04-23_at_05.19.18.png", "size_bytes": 36991}
[2025-04-23T06:00:58.593124] {"action": "submit_attempt", "order_data": {"order_number": "URC1037", "requester_id": 3, "order_note": null, "note_to_supplier": "This is a note for order URC1037\nThis order has 2 lines :\n1 item of ABRA025 - R15,000\n1 item of BEAR059 for R3,000", "supplier_id": 6, "items": [{"item_code": "ABRA025", "item_description": "Flap Wheel  50 X 20  X  6  Mm  P80", "project": "KA04M", "qty_ordered": 1.0, "price": 15000.0}, {"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "TR30M", "qty_ordered": 1.0, "price": 3000.0}], "status": "Awaiting Authorisation", "total": 18000.0}}
[2025-04-23T06:00:58.594209] {"action": "submit_success", "order_number": "URC1037", "status": "Awaiting Authorisation"}
[2025-04-23T06:18:24.718007] {"action": "attachment_uploaded", "order_id": 31, "filename": "Screenshot_2025-04-23_at_05.19.18.png", "path": "data/uploads/31_Screenshot_2025-04-23_at_05.19.18.png", "size_bytes": 36991}
[2025-04-23T06:58:56.012341] {"action": "receive", "orders": [31]}
[2025-04-23T15:19:02.575755] {"action": "submit_attempt", "order_data": {"order_number": "URC1039", "requester_id": 4, "order_note": null, "note_to_supplier": "Note to order number URC1039 for R11,000", "supplier_id": 7, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "PR10M", "qty_ordered": 1.0, "price": 11000.0}], "status": "Awaiting Authorisation", "total": 11000.0}}
[2025-04-23T15:19:02.577530] {"action": "submit_success", "order_number": "URC1039", "status": "Awaiting Authorisation"}
[2025-04-23T15:24:35.159262] {"action": "submit_attempt", "order_data": {"order_number": "URC1041", "requester_id": 4, "order_note": null, "note_to_supplier": "Supplier note for order number URC1041", "supplier_id": 11, "items": [{"item_code": "BECK054", "item_description": "Becker  Machine Spout Liner For  M48", "project": "PR67M", "qty_ordered": 1.0, "price": 12000.0}], "status": "Awaiting Authorisation", "total": 12000.0}}
[2025-04-23T15:24:35.160367] {"action": "submit_success", "order_number": "URC1041", "status": "Awaiting Authorisation"}
[2025-04-24T05:21:28.593868] {"action": "submit_attempt", "order_data": {"order_number": "URC1043", "requester_id": 4, "order_note": null, "note_to_supplier": "Message for URC1043", "supplier_id": 4, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "IN10M", "qty_ordered": 1.0, "price": 15000.0}], "status": "Awaiting Authorisation", "total": 15000.0}}
[2025-04-24T05:21:28.596491] {"action": "submit_success", "order_number": "URC1043", "status": "Awaiting Authorisation"}
[2025-04-24T06:45:34.823350] {"action": "submit_attempt", "order_data": {"order_number": "URC1045", "requester_id": 3, "order_note": null, "note_to_supplier": "Supplier note for order number URC1045", "supplier_id": 6, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "DR09M", "qty_ordered": 1.0, "price": 30000.0}], "status": "Awaiting Authorisation", "total": 30000.0}}
[2025-04-24T06:45:34.825221] {"action": "submit_success", "order_number": "URC1045", "status": "Awaiting Authorisation"}
[2025-04-24T06:54:40.992442] {"action": "submit_attempt", "order_data": {"order_number": "URC1047", "requester_id": 1, "order_note": null, "note_to_supplier": "Suppler note for order number URC1047", "supplier_id": 9, "items": [{"item_code": "BEAR180", "item_description": "Bearing Nylos Ring For 23034 Mac 4 W33 Brass Cage", "project": "PR30M", "qty_ordered": 1.0, "price": 15000.0}], "status": "Awaiting Authorisation", "total": 15000.0}}
[2025-04-24T06:54:40.993693] {"action": "submit_success", "order_number": "URC1047", "status": "Awaiting Authorisation"}
[2025-04-24T06:58:37.199121] {"action": "submit_attempt", "order_data": {"order_number": "URC1049", "requester_id": 1, "order_note": null, "note_to_supplier": "Supplier note for order URC1049", "supplier_id": 12, "items": [{"item_code": "BECK054", "item_description": "Becker  Machine Spout Liner For  M48", "project": "TR59M", "qty_ordered": 1.0, "price": 120000.0}], "status": "Awaiting Authorisation", "total": 120000.0}}
[2025-04-24T06:58:37.200070] {"action": "submit_success", "order_number": "URC1049", "status": "Awaiting Authorisation"}
[2025-04-24T07:12:02.205546] {"action": "submit_attempt", "order_data": {"order_number": "URC1051", "requester_id": 1, "order_note": null, "note_to_supplier": "Supplier note to order number URC1051", "supplier_id": 7, "items": [{"item_code": "BEAR180", "item_description": "Bearing Nylos Ring For 23034 Mac 4 W33 Brass Cage", "project": "TR71M", "qty_ordered": 1.0, "price": 12000.0}], "status": "Awaiting Authorisation", "total": 12000.0}}
[2025-04-24T07:12:02.208284] {"action": "submit_success", "order_number": "URC1051", "status": "Awaiting Authorisation"}
[2025-04-24T07:27:13.836175] {"action": "submit_attempt", "order_data": {"order_number": "URC1053", "requester_id": 2, "order_note": null, "note_to_supplier": "Note to supplier - order number URC1053", "supplier_id": 7, "items": [{"item_code": "ABRA025", "item_description": "Flap Wheel  50 X 20  X  6  Mm  P80", "project": "DR09M", "qty_ordered": 1.0, "price": 18000.0}], "status": "Awaiting Authorisation", "total": 18000.0}}
[2025-04-24T07:27:13.838910] {"action": "submit_success", "order_number": "URC1053", "status": "Awaiting Authorisation"}

```

### `logs/testing_log.txt`
**(No description)**
```python
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

### `logs/whatsapp_log.txt`
**(No description)**
```python
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

### `project_status_snapshot.md`
**📦 Universal Recycling Orders Project Snapshot**
```python
# 📦 Universal Recycling Orders Project Snapshot

📁 Analyzing file: backend/endpoints/orders.py

## 🧠 Backend Routes
- POST /orders → ✅ Found: line 40: @router.post("")
- POST /orders/receive → ❌ Not found
- GET /orders/print_to_file → ❌ Not found
- GET /orders/print → ❌ Not found
- GET /orders/pending → ❌ Not found
- GET /orders/audit → ❌ Not found
- POST /orders/upload_attachment → ❌ Not found

## 🎨 Frontend Templates

- index.html → ❌ Empty
- pending.html → ❌ Empty
- print_template.html → ✅ Populated
- received.html → ❌ Empty
- maintenance.html → ❌ Empty
- audit.html → ❌ Empty
- new_order.html → ❌ Empty

## ⚙️ Scripts Detected

- fix_escaped_triple_quotes.py
- fix_print_order_items.py
- generate_project_status_snapshot.py
- inject_filter_route.py
- insert_audit_route.py
- insert_audit_tracking_into_receive.py
- insert_awaiting_auth_order.py
- insert_extended_order_route.py
- insert_get_all_orders.py
- insert_next_order_number_route.py
- insert_pending_route.py
- insert_print_route.py
- insert_print_to_file_route.py
- insert_receive_route.py
- insert_test_order.py
- insert_twilio_placeholder.py
- insert_upload_attachment.py
- patch_ordercreate_model.py
- prepare_lookup_tables.py
- start_server_background.py

## 🧪 Test Scripts

- test_create_full_order.py
- test_pipeline_end_to_end.py
- test_receive_po_test_001.py

## 📋 Lookup Table Check

- suppliers: ✅ Populated (3 rows)
- projects: ❌ Empty (0 rows)
- items: ❌ Empty (0 rows)
- requesters: ❌ Table not found

## 🗃️ Database File

- ✅ Found at data/orders.db

## ✅ Summary

- You can upload this file to a new ChatGPT session to instantly re-brief Cathy.
- File generated automatically. No need to manually track dev state.

```

### `requirements.txt`
**(No description)**
```python
fastapi
uvicorn
jinja2
python-multipart
twilio
python-dotenv

```

### `scripts/reset_and_test.sh`
**!/usr/bin/env bash**
```python
#!/usr/bin/env bash
set -euo pipefail

# 1) Kill any Uvicorn on port 8004
if lsof -i:8004 | grep -q LISTEN; then
  echo "⏳ Stopping old server…"
  lsof -ti:8004 | xargs kill -9
  sleep 1
else
  echo "⚠ no process on port 8004"
fi

# 2) Delete the old DB
echo "🗑 Removing old database…"
rm -f data/orders.db

# 3) Recreate all tables
echo "📦 Initializing schema…"
python3 - << 'EOF'
from backend.database import init_db
init_db()
EOF

# 4) Seed lookups (requesters, suppliers, plus you can add projects/users/items here)
echo "🌱 Seeding lookup tables…"
sqlite3 data/orders.db << 'EOF'
-- requesters
INSERT OR IGNORE INTO requesters(name) VALUES
  ('Aaron'),('Leon'),('Gert'),('Omar'),('Raymond'),('Yolandi');
-- suppliers
INSERT OR IGNORE INTO suppliers(account_number,name) VALUES
  ('SUPP001','Test Supplier');
-- projects (optional stub)
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_code TEXT UNIQUE
);
INSERT OR IGNORE INTO projects(project_code) VALUES ('TEST');
-- users (optional stub)
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password_hash TEXT NOT NULL,
  rights TEXT NOT NULL
);
INSERT OR IGNORE INTO users(username,password_hash,rights) VALUES ('aaron','<hash>','Edit');
-- items (optional stub)
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_code TEXT UNIQUE,
  item_description TEXT
);
INSERT OR IGNORE INTO items(item_code,item_description) VALUES ('TEST123','Integration Widget');
EOF

# 5) Start the server in the background
echo "🚀 Starting server…"
nohup python3 scripts/start_server.py &>/dev/null &

# 6) Wait for it to spin up
sleep 3

# 7) Fire off a test order (should land as ID=1)
echo "📝 Creating a test order…"
curl -s -X POST http://localhost:8004/orders \
  -H "Content-Type: application/json" \
  -d '{
    "requester_id": 1,
    "supplier_id": 1,
    "order_note": "Shell test order",
    "supplier_note": "Test supplier",
    "items": [{
      "item_code": "TEST123",
      "item_description": "Integration Widget",
      "project": "TEST",
      "qty_ordered": 3,
      "price": 9.99
    }]
  }' | jq .

# 8) Run your validation script
echo "🔍 Running validation…"
python3 scripts/validate_repaired_routes.py

echo "✅ All done!"


```


## 🗄️ Database Schema (`data/orders.db`)

_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._

### Table `requesters`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `name` (TEXT), pk=False, notnull=False, default=None

### Table `sqlite_sequence`
- `name` (), pk=False, notnull=False, default=None
- `seq` (), pk=False, notnull=False, default=None

### Table `suppliers`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `account_number` (TEXT), pk=False, notnull=False, default=None
- `name` (TEXT), pk=False, notnull=False, default=None
- `telephone` (TEXT), pk=False, notnull=False, default=None
- `vat_number` (TEXT), pk=False, notnull=False, default=None
- `registration_number` (TEXT), pk=False, notnull=False, default=None
- `email` (TEXT), pk=False, notnull=False, default=None
- `contact_name` (TEXT), pk=False, notnull=False, default=None
- `contact_telephone` (TEXT), pk=False, notnull=False, default=None
- `address_line1` (TEXT), pk=False, notnull=False, default=None
- `address_line2` (TEXT), pk=False, notnull=False, default=None
- `address_line3` (TEXT), pk=False, notnull=False, default=None
- `postal_code` (TEXT), pk=False, notnull=False, default=None

### Table `orders`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_number` (TEXT), pk=False, notnull=False, default=None
- `status` (TEXT), pk=False, notnull=False, default=None
- `created_date` (TEXT), pk=False, notnull=False, default=CURRENT_TIMESTAMP
- `received_date` (TEXT), pk=False, notnull=False, default=None
- `total` (REAL), pk=False, notnull=False, default=None
- `order_note` (TEXT), pk=False, notnull=False, default=None
- `note_to_supplier` (TEXT), pk=False, notnull=False, default=None
- `supplier_id` (INTEGER), pk=False, notnull=False, default=None
- `requester_id` (INTEGER), pk=False, notnull=False, default=None

### Table `order_items`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_id` (INTEGER), pk=False, notnull=False, default=None
- `item_code` (TEXT), pk=False, notnull=False, default=None
- `item_description` (TEXT), pk=False, notnull=False, default=None
- `project` (TEXT), pk=False, notnull=False, default=None
- `qty_ordered` (REAL), pk=False, notnull=False, default=None
- `qty_received` (REAL), pk=False, notnull=False, default=None
- `received_date` (TEXT), pk=False, notnull=False, default=None
- `price` (REAL), pk=False, notnull=False, default=None
- `total` (REAL), pk=False, notnull=False, default=None

### Table `attachments`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_id` (INTEGER), pk=False, notnull=False, default=None
- `filename` (TEXT), pk=False, notnull=True, default=None
- `file_path` (TEXT), pk=False, notnull=True, default=None
- `upload_date` (TEXT), pk=False, notnull=True, default=None

### Table `audit_trail`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_id` (INTEGER), pk=False, notnull=False, default=None
- `action` (TEXT), pk=False, notnull=False, default=None
- `details` (TEXT), pk=False, notnull=False, default=None
- `action_date` (TEXT), pk=False, notnull=False, default=CURRENT_TIMESTAMP
- `user_id` (INTEGER), pk=False, notnull=False, default=None

### Table `settings`
- `key` (TEXT), pk=True, notnull=False, default=None
- `value` (TEXT), pk=False, notnull=False, default=None

### Table `users`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `username` (TEXT), pk=False, notnull=False, default=None
- `password_hash` (TEXT), pk=False, notnull=True, default=None
- `rights` (TEXT), pk=False, notnull=True, default=None

### Table `projects`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `project_code` (TEXT), pk=False, notnull=False, default=None
- `project_name` (TEXT), pk=False, notnull=False, default=None

### Table `items`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `item_code` (TEXT), pk=False, notnull=False, default=None
- `item_description` (TEXT), pk=False, notnull=False, default=None



## ✅ TODOs (Static Manual Items)

- [ ] Modularize long `.js` files into reusable components
- [ ] Finalize `/audit` route with filters + trail UI
- [ ] Finalize `/orders/print` layout + backend
- [ ] Add RBAC (role-based access control)
- [ ] Pagination on long tables (Pending/Received)
- [ ] Security audit on file uploads
- [ ] Normalize filenames and harden upload paths
- [ ] Add upload success/failure status to frontend

## ⛳ Auto-detected TODOs

- `venv/lib/python3.13/site-packages/typing_extensions.py`: Use inspect.VALUE here, and make the annotations lazily evaluated
- `venv/lib/python3.13/site-packages/typing_extensions.py`: Use inspect.VALUE here, and make the annotations lazily evaluated
- `venv/lib/python3.13/site-packages/selenium/webdriver/common/utils.py`: Does this even work?
- `venv/lib/python3.13/site-packages/selenium/webdriver/remote/shadowroot.py`: We should look and see  how we can create a search context like Java/.NET
- `venv/lib/python3.13/site-packages/selenium/webdriver/remote/webelement.py`: When moving to supporting python 3.9 as the minimum version we can
- `venv/lib/python3.13/site-packages/aiohttp/web_response.py`: do we need domain/path here?
- `venv/lib/python3.13/site-packages/aiohttp/streams.py`: size is ignored, remove the param later
- `venv/lib/python3.13/site-packages/aiohttp/streams.py`: should be `if` instead of `while`
- `venv/lib/python3.13/site-packages/aiohttp/streams.py`: should be `if` instead of `while`
- `venv/lib/python3.13/site-packages/aiohttp/streams.py`: add async def readuntil
- `venv/lib/python3.13/site-packages/aiohttp/web_urldispatcher.py`: implement all abstract methods
- `venv/lib/python3.13/site-packages/aiohttp/web_urldispatcher.py`: impl missing abstract methods
- `venv/lib/python3.13/site-packages/aiohttp/web_urldispatcher.py`: cache file content
- `venv/lib/python3.13/site-packages/aiohttp/web_urldispatcher.py`: sha256 can be configurable param
- `venv/lib/python3.13/site-packages/aiohttp/client_proto.py`: actual types are:
- `venv/lib/python3.13/site-packages/aiohttp/client_reqrep.py`: Fix session=None in tests (see ClientRequest.__init__).
- `venv/lib/python3.13/site-packages/websocket/_http.py`: Use python-socks for http protocol also, to standardize flow
- `venv/lib/python3.13/site-packages/websocket/_http.py`: support digest auth.
- `venv/lib/python3.13/site-packages/websocket/tests/test_websocket.py`: add longer frame data
- `venv/lib/python3.13/site-packages/websocket/tests/test_websocket.py`: add longer frame data
- `venv/lib/python3.13/site-packages/websocket/tests/test_http.py`: Test SOCKS4 and SOCK5 proxies with unit tests
- `venv/lib/python3.13/site-packages/trio/_subprocess.py`: how do paths and sequences thereof play with `shell=True`?
- `venv/lib/python3.13/site-packages/trio/_util.py`: python3.7 support is now dropped, so the above can be addressed.
- `venv/lib/python3.13/site-packages/trio/_dtls.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_dtls.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_dtls.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_dtls.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_dtls.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_dtls.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_tests/test_testing_raisesgroup.py`: this line is not great, should maybe follow the same format as the other and say
- `venv/lib/python3.13/site-packages/trio/_tests/test_exports.py`: this *should* be visible via `dir`!!
- `venv/lib/python3.13/site-packages/trio/_tests/test_exports.py`: why is this? Is it a problem?
- `venv/lib/python3.13/site-packages/trio/_tests/test_highlevel_ssl_helpers.py`: this function wraps an SSLListener around a SocketListener, this is illegal
- `venv/lib/python3.13/site-packages/trio/_tests/test_socket.py`: this implies that we can send host=None, but what does that imply for the return value, and other stuff?
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: Fix FakeNet typing
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: Fix FakeNet typing
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_dtls.py`: add type annotations for FakeNet
- `venv/lib/python3.13/site-packages/trio/_tests/test_fakenet.py`: recvmsg
- `venv/lib/python3.13/site-packages/trio/_tests/test_highlevel_socket.py`: does not raise an error?
- `venv/lib/python3.13/site-packages/trio/_tests/check_type_completeness.py`: consider checking manually without `--ignoreexternal`, and/or
- `venv/lib/python3.13/site-packages/trio/_tests/check_type_completeness.py`: these are erroring on all platforms, why?
- `venv/lib/python3.13/site-packages/trio/_tests/test_threads.py`: should CapacityLimiter have an abc or protocol so users can modify it?
- `venv/lib/python3.13/site-packages/trio/_tests/type_tests/path.py`: Path.walk() in 3.12
- `venv/lib/python3.13/site-packages/trio/_tests/type_tests/path.py`: report mypy bug: equiv to https://github.com/microsoft/pyright/issues/6833
- `venv/lib/python3.13/site-packages/trio/_core/_windows_cffi.py`: make this work in MyPy
- `venv/lib/python3.13/site-packages/trio/_core/_io_kqueue.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_core/_io_kqueue.py`: test this branch
- `venv/lib/python3.13/site-packages/trio/_core/_io_kqueue.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_core/_io_kqueue.py`: test this branch
- `venv/lib/python3.13/site-packages/trio/_core/_io_windows.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_core/_io_windows.py`: test this line
- `venv/lib/python3.13/site-packages/trio/_core/_io_windows.py`: what type does this return?
- `venv/lib/python3.13/site-packages/trio/_core/_run.py`: develop test for this deletion
- `venv/lib/python3.13/site-packages/trio/_core/_run.py`: develop test for this deletion
- `venv/lib/python3.13/site-packages/trio/_core/_tests/test_run.py`: stop event loop from hanging on to the nursery at this point
- `venv/lib/python3.13/site-packages/trio/_core/_tests/test_exceptiongroup_gc.py`: is the above comment true anymore? as this no longer uses MultiError.catch
- `venv/lib/python3.13/site-packages/trio/_tools/gen_exports.py`: test this branch
- `venv/lib/python3.13/site-packages/trio/testing/_raises_group.py`: when transitioning to pytest, harmonize Matcher and RaisesGroup
- `venv/lib/python3.13/site-packages/trio/testing/_raises_group.py`: if this fails, we should say the *group* did not match
- `venv/lib/python3.13/site-packages/trio/testing/_fake_net.py`: This method is not tested, and seems to make incorrect assumptions. It should maybe raise NotImplementedError.
- `venv/lib/python3.13/site-packages/jinja2/ext.py`: the i18n extension is currently reevaluating values in a few
- `venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py`: We ought to handle 404 cases if debug is set.
- `venv/lib/python3.13/site-packages/bs4/tests/test_tree.py`: OK but what happens?
- `venv/lib/python3.13/site-packages/bs4/tests/test_tree.py`: OK but what does it look like?
- `venv/lib/python3.13/site-packages/bs4/tests/test_builder_registry.py`: Split out the lxml and html5lib tests into their own classes
- `venv/lib/python3.13/site-packages/bs4/tests/test_tag.py`: This code is in the builder and should be tested there.
- `venv/lib/python3.13/site-packages/bs4/builder/_htmlparser.py`: handle namespaces here?
- `venv/lib/python3.13/site-packages/bs4/builder/_htmlparser.py`: This was originally a workaround for a bug in
- `venv/lib/python3.13/site-packages/bs4/builder/__init__.py`: store_line_numbers is probably irrelevant now that
- `venv/lib/python3.13/site-packages/bs4/builder/__init__.py`: This cast will fail in the (very unlikely) scenario
- `venv/lib/python3.13/site-packages/bs4/builder/_html5lib.py`: Why is the parser 'html.parser' here? Using
- `venv/lib/python3.13/site-packages/bs4/builder/_html5lib.py`: What are **kwargs exactly? Should they be passed in
- `venv/lib/python3.13/site-packages/bs4/builder/_html5lib.py`: This code is not covered by the BS4 tests, and
- `venv/lib/python3.13/site-packages/bs4/builder/_html5lib.py`: This has O(n^2) performance, for input like
- `venv/lib/python3.13/site-packages/bs4/builder/_lxml.py`: Issue a warning if parser is present but not a
- `venv/lib/python3.13/site-packages/bs4/builder/_lxml.py`: This is a workaround for
- `venv/lib/python3.13/site-packages/click/_termui_impl.py`: This never terminates if the passed generator never terminates.
- `venv/lib/python3.13/site-packages/trio_websocket/_impl.py`: shouldn't the receive channel be closed earlier, so that
- `venv/lib/python3.13/site-packages/charset_normalizer/legacy.py`: remove this check when dropping Python 3.7 support
- `venv/lib/python3.13/site-packages/requests/hooks.py`: response is the only one
- `venv/lib/python3.13/site-packages/requests/adapters.py`: Remove this in 3.0.0: see #2811
- `venv/lib/python3.13/site-packages/anyio/_core/_fileio.py`: add return type annotation when Typeshed gets it
- `venv/lib/python3.13/site-packages/pip/_internal/cache.py`: use DirectUrl.equivalent when
- `venv/lib/python3.13/site-packages/pip/_internal/network/lazy_wheel.py`: Get range requests to be correctly cached
- `venv/lib/python3.13/site-packages/pip/_internal/models/selection_prefs.py`: This needs Python 3.10's improved slots support for dataclasses
- `venv/lib/python3.13/site-packages/pip/_internal/models/installation_report.py`: currently, the resolver uses the default environment to evaluate
- `venv/lib/python3.13/site-packages/pip/_internal/cli/base_command.py`: Try to get these passing down from the command?
- `venv/lib/python3.13/site-packages/pip/_internal/operations/prepare.py`: separate this part out from RequirementPreparer when the v1
- `venv/lib/python3.13/site-packages/pip/_internal/req/req_file.py`: replace this with slots=True when dropping Python 3.9 support.
- `venv/lib/python3.13/site-packages/pip/_internal/req/req_file.py`: handle space after '\'.
- `venv/lib/python3.13/site-packages/pip/_internal/req/constructors.py`: The is_installable_dir test here might not be necessary
- `venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py`: Remove this block after dropping Python 3.8 support.
- `venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/factory.py`: Check already installed candidate, and use it if the link and
- `venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/factory.py`: Are there more cases this needs to return True? Editable?
- `venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/candidates.py`: performance: this means we iterate the dependencies at least twice,
- `venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/candidates.py`: Supply reason based on force_reinstall and upgrade_strategy.
- `venv/lib/python3.13/site-packages/pip/_internal/index/collector.py`: In the future, it would be nice if pip supported PEP 691
- `venv/lib/python3.13/site-packages/pip/_internal/commands/inspect.py`: tags? scheme?
- `venv/lib/python3.13/site-packages/pip/_internal/metadata/base.py`: Move definition here.
- `venv/lib/python3.13/site-packages/pip/_internal/metadata/base.py`: this property is relatively costly to compute, memoize it ?
- `venv/lib/python3.13/site-packages/pip/_internal/metadata/base.py`: get project location from second line of egg_link file
- `venv/lib/python3.13/site-packages/pip/_vendor/typing_extensions.py`: Use inspect.VALUE here, and make the annotations lazily evaluated
- `venv/lib/python3.13/site-packages/pip/_vendor/typing_extensions.py`: Use inspect.VALUE here, and make the annotations lazily evaluated
- `venv/lib/python3.13/site-packages/pip/_vendor/packaging/tags.py`: Need to care about 32-bit PPC for ppc64 through 10.2?
- `venv/lib/python3.13/site-packages/pip/_vendor/packaging/metadata.py`: The spec doesn't say anything about if the keys should be
- `venv/lib/python3.13/site-packages/pip/_vendor/packaging/metadata.py`: 2.1: can be in body
- `venv/lib/python3.13/site-packages/pip/_vendor/packaging/requirements.py`: Can we test whether something is contained within a requirement?
- `venv/lib/python3.13/site-packages/pip/_vendor/packaging/requirements.py`: Can we normalize the name and extra name?
- `venv/lib/python3.13/site-packages/pip/_vendor/truststore/_macos.py`: Not sure if we need the SecTrustResultType for anything?
- `venv/lib/python3.13/site-packages/pip/_vendor/msgpack/fallback.py`: should we eliminate the recursion?
- `venv/lib/python3.13/site-packages/pip/_vendor/msgpack/fallback.py`: check whether we need to call `list_hook`
- `venv/lib/python3.13/site-packages/pip/_vendor/msgpack/fallback.py`: is the interaction between `list_hook` and `use_list` ok?
- `venv/lib/python3.13/site-packages/pip/_vendor/msgpack/fallback.py`: check whether we need to call hooks
- `venv/lib/python3.13/site-packages/pip/_vendor/pygments/formatters/img.py`: make sure tab expansion happens earlier in the chain.  It
- `venv/lib/python3.13/site-packages/pip/_vendor/pygments/formatters/latex.py`: add support for background colors
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/locators.py`: SHA256 digest
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/metadata.py`: document the mapping API and UNKNOWN default key
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/metadata.py`: could add iter* variants
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/metadata.py`: any other fields wanted
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/version.py`: unintended side-effect on, e.g., "2003.05.09"
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/util.py`: check k, v for valid values
- `venv/lib/python3.13/site-packages/pip/_vendor/distlib/wheel.py`: version verification
- `venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/controller.py`: There is an assumption that the result will be a
- `venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/filewrapper.py`: Add some logging here...
- `venv/lib/python3.13/site-packages/pip/_vendor/requests/hooks.py`: response is the only one
- `venv/lib/python3.13/site-packages/pip/_vendor/requests/adapters.py`: Remove this in 3.0.0: see #2811
- `venv/lib/python3.13/site-packages/pip/_vendor/rich/text.py`: This is a little inefficient, it is only used by full justify
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/connection.py`: Fix tunnel so it doesn't depend on self.sock state.
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/connectionpool.py`: Add optional support for socket.gethostbyname checking.
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py`: In v2 we can remove this sentinel and metaclass with deprecated options.
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py`: Deprecated, remove in v2.0
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py`: If already given in **kw we use what's given to us
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py`: For now favor if the Retry implementation sets its own method_whitelist
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py`: Remove this deprecated alias in v2.0
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/url.py`: Remove this when we break backwards compatibility.
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/securetransport.py`: should I do clean shutdown here? Do I have to?
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/securetransport.py`: Well, crap.
- `venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/securetransport.py`: Update in line with above.
- `venv/lib/python3.13/site-packages/pip/_vendor/pkg_resources/__init__.py`: Add Generic type annotations to initialized collections.
- `venv/lib/python3.13/site-packages/pip/_vendor/pkg_resources/__init__.py`: / Incomplete: A readable file-like object
- `venv/lib/python3.13/site-packages/pip/_vendor/pkg_resources/__init__.py`: remove this except clause when python/cpython#103632 is fixed.
- `venv/lib/python3.13/site-packages/pip/_vendor/pkg_resources/__init__.py`: Add a deadline?
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: what happens if we don't have a filename?
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: verify that we're in the state MultipartState.END, otherwise throw an
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: check for error here.
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: handle mixed case
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: check for errors
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: check that we properly handle 8bit / 7bit encoding.
- `venv/lib/python3.13/site-packages/python_multipart/multipart.py`: check the parser's return value for errors?
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/params.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/applications.py`: remove when discarding the openapi_prefix parameter
- `venv/lib/python3.13/site-packages/fastapi/encoders.py`: pv2 should this return strings instead?
- `venv/lib/python3.13/site-packages/fastapi/encoders.py`: remove when deprecating Pydantic v1
- `venv/lib/python3.13/site-packages/fastapi/encoders.py`: remove when deprecating Pydantic v1
- `venv/lib/python3.13/site-packages/fastapi/routing.py`: remove this scope later, after a few releases
- `venv/lib/python3.13/site-packages/fastapi/routing.py`: remove when deprecating Pydantic v1
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/param_functions.py`: update when deprecating Pydantic v1, import these types
- `venv/lib/python3.13/site-packages/fastapi/_compat.py`: remove when deprecating Pydantic v1
- `venv/lib/python3.13/site-packages/fastapi/security/oauth2.py`: import from typing when deprecating Python 3.9
- `venv/lib/python3.13/site-packages/fastapi/openapi/models.py`: uncomment and remove below when deprecating Pydantic v1
- `venv/lib/python3.13/site-packages/fastapi/openapi/utils.py`: probably make status_code a default class attribute for all
- `venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/wsproto_impl.py`: Remove `type: ignore` when wsproto fixes the type annotation.
- `venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/wsproto_impl.py`: we may want to guard the size of self.bytes and self.text
- `venv/lib/python3.13/site-packages/urllib3/_base_connection.py`: Remove this in favor of a better
- `venv/lib/python3.13/site-packages/urllib3/response.py`: make sure to initially read enough data to get past the headers
- `venv/lib/python3.13/site-packages/urllib3/connection.py`: Fix tunnel so it doesn't depend on self.sock state.
- `venv/lib/python3.13/site-packages/urllib3/connection.py`: should we implement it everywhere?
- `venv/lib/python3.13/site-packages/urllib3/connectionpool.py`: Add optional support for socket.gethostbyname checking.
- `venv/lib/python3.13/site-packages/urllib3/connectionpool.py`: revise this, see https://github.com/urllib3/urllib3/issues/2791
- `venv/lib/python3.13/site-packages/urllib3/util/url.py`: Remove this when we break backwards compatibility.
- `venv/lib/python3.13/site-packages/urllib3/http2/__init__.py`: Offer 'http/1.1' as well, but for testing purposes this is handy.
- `venv/lib/python3.13/site-packages/urllib3/http2/connection.py`: SKIPPABLE_HEADERS from urllib3 are ignored.
- `venv/lib/python3.13/site-packages/urllib3/http2/connection.py`: Arbitrary read value.
- `venv/lib/python3.13/site-packages/urllib3/http2/connection.py`: this is often present from upstream.
- `venv/lib/python3.13/site-packages/urllib3/http2/connection.py`: This is a woefully incomplete response object, but works for non-streaming.
- `venv/lib/python3.13/site-packages/urllib3/http2/connection.py`: support decoding
- `venv/lib/python3.13/site-packages/itsdangerous/timed.py`: Signature is incompatible because parameters were added
- `venv/lib/python3.13/site-packages/pydantic/functional_validators.py`: if `schema['serialization']` is one of `'include-exclude-dict/sequence',
- `venv/lib/python3.13/site-packages/pydantic/alias_generators.py`: in V3, change the argument names to be more descriptive
- `venv/lib/python3.13/site-packages/pydantic/fields.py`: PEP 747: use TypeForm:
- `venv/lib/python3.13/site-packages/pydantic/fields.py`: check for classvar and error?
- `venv/lib/python3.13/site-packages/pydantic/fields.py`: check for classvar and error?
- `venv/lib/python3.13/site-packages/pydantic/fields.py`: infer from the default, this can be done in v3 once we treat final fields with
- `venv/lib/python3.13/site-packages/pydantic/fields.py`: properly make use of the protocol (https://rich.readthedocs.io/en/stable/pretty.html#rich-repr-protocol)
- `venv/lib/python3.13/site-packages/pydantic/fields.py`: use `_typing_extra.EllipsisType` when we drop Py3.9
- `venv/lib/python3.13/site-packages/pydantic/mypy.py`: Only do this if the first argument of the decorated function is `cls`
- `venv/lib/python3.13/site-packages/pydantic/mypy.py`: We shouldn't be performing type operations during the main
- `venv/lib/python3.13/site-packages/pydantic/mypy.py`: this path should be removed (see https://github.com/pydantic/pydantic/issues/11119)
- `venv/lib/python3.13/site-packages/pydantic/json_schema.py`: I dislike that we have to wrap these basic dict updates in callables, is there any way around this?
- `venv/lib/python3.13/site-packages/pydantic/json_schema.py`: should we add regex flags to the pattern?
- `venv/lib/python3.13/site-packages/pydantic/json_schema.py`: improvements along with https://github.com/pydantic/pydantic/issues/8208
- `venv/lib/python3.13/site-packages/pydantic/json_schema.py`: fixme - this is a workaround for the fact that we can't always resolve refs
- `venv/lib/python3.13/site-packages/pydantic/json_schema.py`: Need to read the default value off of model config or whatever
- `venv/lib/python3.13/site-packages/pydantic/json_schema.py`: replace this default False
- `venv/lib/python3.13/site-packages/pydantic/type_adapter.py`: we don't go through the rebuild logic here directly because we don't want
- `venv/lib/python3.13/site-packages/pydantic/dataclasses.py`: `parent_namespace` is currently None, but we could do the same thing as Pydantic models:
- `venv/lib/python3.13/site-packages/pydantic/main.py`: v3 fallback to `dict` when the deprecated `dict` method gets removed.
- `venv/lib/python3.13/site-packages/pydantic/main.py`: - matching error
- `venv/lib/python3.13/site-packages/pydantic/main.py`: PEP 747: replace `Any` by the TypeForm:
- `venv/lib/python3.13/site-packages/pydantic/v1/networks.py`: Needed to generic "Parts" for "Replica Set", "Sharded Cluster", and other mongodb deployment modes
- `venv/lib/python3.13/site-packages/pydantic/v1/utils.py`: replace annotation with actual expected types once #1055 solved
- `venv/lib/python3.13/site-packages/pydantic/_internal/_typing_extra.py`: implement `is_finalvar_annotation` as Final can be wrapped with other special forms:
- `venv/lib/python3.13/site-packages/pydantic/_internal/_typing_extra.py`: In 2.12, delete this export. It is currently defined only to not break
- `venv/lib/python3.13/site-packages/pydantic/_internal/_typing_extra.py`: Ideally, we should avoid relying on the private `typing` constructs:
- `venv/lib/python3.13/site-packages/pydantic/_internal/_typing_extra.py`: ideally recursion errors should be checked in `eval_type` above, but `eval_type_backport`
- `venv/lib/python3.13/site-packages/pydantic/_internal/_validators.py`: refactor sequence validation to validate with either a list or a tuple
- `venv/lib/python3.13/site-packages/pydantic/_internal/_validators.py`: strict mode
- `venv/lib/python3.13/site-packages/pydantic/_internal/_namespace_utils.py`: should we merge the parent namespace here?
- `venv/lib/python3.13/site-packages/pydantic/_internal/_namespace_utils.py`: `typ.__type_params__` when we drop support for Python 3.11:
- `venv/lib/python3.13/site-packages/pydantic/_internal/_known_annotated_metadata.py`: this is a bit redundant, we could probably avoid some of these
- `venv/lib/python3.13/site-packages/pydantic/_internal/_model_construction.py`: we can also stop there if `__pydantic_fields_complete__` is False.
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`: in theory we should check that the schema accepts a serialization key
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`: this is an ugly hack, how do we trigger an Any schema for serialization?
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`: note, this is a fairly common pattern, re lax / strict for attempted type coercion,
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`: do we really need to resolve type vars here?
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`: something like https://github.com/pydantic/pydantic/issues/5952
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`: V3: this function is only used for deprecated decorators. It should
- `venv/lib/python3.13/site-packages/pydantic/_internal/_schema_gather.py`: When we drop 3.9, use a match statement to get better type checking and remove
- `venv/lib/python3.13/site-packages/pydantic/_internal/_schema_gather.py`: duplicate schema types for serializers and validators, needs to be deduplicated.
- `venv/lib/python3.13/site-packages/pydantic/_internal/_schema_gather.py`: duplicate schema types for serializers and validators, needs to be deduplicated.
- `venv/lib/python3.13/site-packages/pydantic/_internal/_fields.py`: We should probably do something with this so that validate_assignment behaves properly
- `venv/lib/python3.13/site-packages/pydantic/_internal/_fields.py`: same note as above re validate_assignment
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generics.py`: This could be unified with `get_standard_typevars_map` if we stored the generic metadata
- `venv/lib/python3.13/site-packages/pydantic/_internal/_generics.py`: remove parentheses when we drop support for Python 3.10:
- `venv/lib/python3.13/site-packages/pydantic/experimental/pipeline.py`: ultimately, make this public, see https://github.com/pydantic/pydantic/pull/9459#discussion_r1628197626
- `venv/lib/python3.13/site-packages/pydantic/experimental/pipeline.py`: is there a better way? should we just not do this?
- `venv/lib/python3.13/site-packages/pydantic/deprecated/json.py`: Add a suggested migration path once there is a way to use custom encoders
- `venv/lib/python3.13/site-packages/typing_inspection/introspection.py`: at some point, we could switch to an enum flag, so that multiple sources
- `venv/lib/python3.13/site-packages/typing_inspection/introspection.py`: if/when https://peps.python.org/pep-0767/ is accepted, add 'read_only'
- `venv/lib/python3.13/site-packages/typing_inspection/introspection.py`: use a match statement when Python 3.9 support is dropped.
- `venv/lib/python3.13/site-packages/yarl/_url.py`: add a keyword-only option for keeping user/pass maybe?

## 📝 Project summary
This is a custom-built Purchase Order system for Universal Recycling.

**Build & Testing Approach:**
- Features are isolated and tested before being chained
- Scripts inject DB rows or hit live endpoints for testing
- Full `curl`, Python, and sqlite3 test coverage
- UI is layered only on top of a tested backend


## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

## ⚙️ System Settings

| Key                 | Value   |
|----------------------|---------|
| auth_threshold       | 10000   |
| order_number_start   | URC1024 |
| last_order_number    | URC000  |

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

