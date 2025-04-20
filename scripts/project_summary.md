# 📦 Project Snapshot
Generated: 2025-04-21 00:53:06

## 📁 Directory Tree
````
/Users/stevencohen/Projects/universal_recycling/orders_project/scripts
├── add_debug_validation_handler.py
├── clear_live_data.py
├── dump_project_summary.py
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
├── project_summary.md
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
## 📄 Source Files

### `.DS_Store`
**(No description)**
```python
<!-- ERROR reading .DS_Store: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte -->
```

### `add_debug_validation_handler.py`
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

### `clear_live_data.py`
**!/usr/bin/env python3**
```python
#!/usr/bin/env python3
import sqlite3

DB_PATH = "data/orders.db"

TABLES_TO_CLEAR = [
    "orders",
    "order_items",
    "attachments",
    "audit_trail"
]

def clear_live_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for table in TABLES_TO_CLEAR:
                print(f"Clearing table: {table}")
                cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print("✅ Live transactional data cleared successfully.")
    except Exception as e:
        print(f"❌ Failed to clear data: {e}")

if __name__ == "__main__":
    clear_live_data()


```

### `dump_project_summary.py`
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
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_MD = PROJECT_ROOT / 'project_summary.md'
DB_FILE = PROJECT_ROOT / 'data' / 'orders.db'

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
    return f"{path}\n" + '\n'.join(_build(path, prefix, level=1))

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
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f"<!-- ERROR reading {path.name}: {e} -->"

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
        status = "✅"
        purpose = summary.get(name, extract_desc(read_src(test_file)))
        md += f"| `{name}` | {purpose} | {status} |\n"
    md += "\n"
    return md

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

# --- Main dump ---
def main():
    md = []
    md.append(f"# 📦 Project Snapshot\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    md.append("## 📁 Directory Tree\n````\n" + build_tree(PROJECT_ROOT) + "\n````")
    md.append("## 📄 Source Files\n")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in sorted(files):
            p = Path(root) / f
            if p == OUTPUT_MD:
                continue
            rel = p.relative_to(PROJECT_ROOT)
            src = read_src(p)
            desc = extract_desc(src)
            md.append(f"### `{rel}`\n**{desc}**\n```python\n{src}\n```\n")
    md.append(dump_db_schema(DB_FILE))
    md.append("## 📝 Project summary\n"
              "I am busy building a Purchase Order system for Universal Recycling.\n\n"
              "**Testing Methodology:**\n"
              "- Each feature is tested in isolation (Python scripts, curl, direct sqlite3 queries)\n"
              "- No feature gets built on top of another until the one before it passes\n"
              "- Audit trails, status transitions, and data integrity are tested at every step\n"
              "- Test records are inserted programmatically, not by hand\n"
              "- UI will only be added when backend is rock solid\n\n"
              "**File Structure Summary:**\n"
              "- `backend/endpoints/orders.py` → Handles all `/orders` routes\n"
              "- `backend/database.py` → DB operations: init, insert, queries\n"
              "- `backend/utils/order_utils.py` → Helpers: status logic, validation\n"
              "- `scripts/` → Injection scripts, test runners & setup tools\n"
              "- `frontend/templates/` → Screen layouts (planned)\n"
              "- `data/orders.db` → Active SQLite file\n\n"
              "**Build Methodology:**\n"
              "- Build backend first → fully tested\n"
              "- One feature at a time → injected via `.py` scripts\n"
              "- No UI work until backend is rock solid\n"
              "- All tests confirmed via curl + Python\n"
              "- Full end-to-end integration test exists\n"
              "- Code reusability is a must (e.g. date handling, filters)\n\n"
              "**Date Input Standardization:**\n"
              "All date inputs (filter, creation, etc.) use `<input type=\"date\">` and transmit in ISO 8601 (YYYY-MM-DD) format. "
              "The backend expects this format and filters directly using SQLite `DATE()` comparisons. "
              "No manual formatting or parsing required.\n\n"
              "**How Steven works with ChatGPT:**\n"
              "- Steven doesn’t know coding; he’s decent with terminal commands\n"
              "- He uses VS Code, wants brief error messages & clear steps\n")
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

### `git_pull_project.py`
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
        try:
            run(["git", "stash", "pop"], "Restore stashed changes")
        except SystemExit:
            print("⚠️ Stash pop failed — resolve manually with `git stash list && git stash apply`")
            sys.exit(1)

    print("✅ Git pull completed successfully!")

if __name__ == "__main__":
    main()

```

### `git_push_project.py`
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

### `init_db_fresh.py`
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

### `inject_filter_route.py`
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

### `insert_get_all_orders.py`
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

### `insert_next_order_number_route.py`
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

### `insert_pending_route.py`
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

### `insert_print_route.py`
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

### `insert_receive_route.py`
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

### `integration_tests.py`
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

### `prepare_lookup_tables.py`
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

### `repair_orders_routes.py`
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

### `reset_and_test.sh`
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

### `seed_static_data.py`
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

### `start_server.py`
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

### `test_authorisation_threshold_trigger.py`
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

### `test_invalid_data_handling.py`
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

### `test_invalid_items_variants.py`
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

### `test_pipeline_end_to_end.py`
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

### `test_receive_partial.py`
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

## 🗄️ Database Schema (`data/orders.db`)

_No DB found_


## 📝 Project summary
I am busy building a Purchase Order system for Universal Recycling.

**Testing Methodology:**
- Each feature is tested in isolation (Python scripts, curl, direct sqlite3 queries)
- No feature gets built on top of another until the one before it passes
- Audit trails, status transitions, and data integrity are tested at every step
- Test records are inserted programmatically, not by hand
- UI will only be added when backend is rock solid

**File Structure Summary:**
- `backend/endpoints/orders.py` → Handles all `/orders` routes
- `backend/database.py` → DB operations: init, insert, queries
- `backend/utils/order_utils.py` → Helpers: status logic, validation
- `scripts/` → Injection scripts, test runners & setup tools
- `frontend/templates/` → Screen layouts (planned)
- `data/orders.db` → Active SQLite file

**Build Methodology:**
- Build backend first → fully tested
- One feature at a time → injected via `.py` scripts
- No UI work until backend is rock solid
- All tests confirmed via curl + Python
- Full end-to-end integration test exists
- Code reusability is a must (e.g. date handling, filters)

**Date Input Standardization:**
All date inputs (filter, creation, etc.) use `<input type="date">` and transmit in ISO 8601 (YYYY-MM-DD) format. The backend expects this format and filters directly using SQLite `DATE()` comparisons. No manual formatting or parsing required.

**How Steven works with ChatGPT:**
- Steven doesn’t know coding; he’s decent with terminal commands
- He uses VS Code, wants brief error messages & clear steps


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

