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
