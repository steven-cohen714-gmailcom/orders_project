import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime

def run_command(command, desc):
    print(f"Running: {desc}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {desc}: {e.stderr}")
        return ""

def get_database_schema(db_path):
    print(f"Fetching database schema from {db_path}")
    schema = ""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                schema += f"\n### Table `{table_name}`\n"
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    col_notnull = "not null" if col[3] else "nullable"
                    col_default = f" default {col[4]}" if col[4] is not None else ""
                    col_pk = "pk=True" if col[5] else "pk=False"
                    schema += f"- `{col_name}` ({col_type}), {col_pk}, {col_notnull}{col_default}\n"
    except sqlite3.Error as e:
        print(f"Error fetching schema: {e}")
        schema += f"Error fetching schema: {e}\n"
    return schema

def get_file_snippet(file_path, snippet_marker=None, max_lines=100):
    print(f"Reading file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if snippet_marker:
                lines = content.split('\n')
                snippet = []
                for line in lines:
                    if snippet_marker in line:
                        snippet.append(line)
                        break
                if not snippet:
                    return f"No snippet found for marker '{snippet_marker}' in {file_path}\n"
                start_idx = lines.index(snippet[0])
                for line in lines[start_idx + 1:]:
                    if line.strip() and not (line.startswith('def ') or line.startswith('@')):
                        snippet.append(line)
                    else:
                        break
                return '\n'.join(snippet)
            else:
                lines = content.split('\n')[:max_lines]
                return '\n'.join(lines)
    except FileNotFoundError:
        return f"File not found: {file_path}\n"
    except Exception as e:
        return f"Error reading {file_path}: {e}\n"

def get_full_file_content(file_path):
    print(f"Reading full file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {file_path}\n"
    except Exception as e:
        return f"Error reading {file_path}: {e}\n"

def get_log_snippet(log_file, max_lines=20):
    print(f"Reading log file: {log_file}")
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Get the last max_lines entries
            return ''.join(lines[-max_lines:])
    except FileNotFoundError:
        return f"Log file not found: {log_file}\n"
    except Exception as e:
        return f"Error reading {log_file}: {e}\n"

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    output_file = repo_path / "project_summary.md"
    db_path = repo_path / "data/orders.db"
    env_path = repo_path / ".env"

    # Header
    intro = f"""# 📦 Project Snapshot

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

"""

    # Directory Tree (depth 5 to capture components)
    dir_structure = "## 📁 Directory Tree\n```\n"
    dir_structure += run_command(["tree", "-L", "5"], "Fetching directory structure")
    dir_structure += "```\n"

    # Python Files (excluding scripts directory)
    python_files = "## 📂 Python Files (Excluding scripts/ Directory)\n"

    # backend/__init__.py
    python_files += "### `backend/__init__.py`\n**Package Initializer**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/__init__.py")
    python_files += "\n```\n"

    # backend/endpoints/__init__.py
    python_files += "### `backend/endpoints/__init__.py`\n**Package Initializer**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/endpoints/__init__.py")
    python_files += "\n```\n"

    # backend/twilio/__init__.py
    python_files += "### `backend/twilio/__init__.py`\n**Package Initializer**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/twilio/__init__.py")
    python_files += "\n```\n"

    # backend/utils/__init__.py
    python_files += "### `backend/utils/__init__.py`\n**Package Initializer**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/utils/__init__.py")
    python_files += "\n```\n"

    # backend/database.py
    python_files += "### `backend/database.py`\n**CREATE TABLE IF NOT EXISTS**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/database.py", "CREATE TABLE IF NOT EXISTS", max_lines=100)
    python_files += "\n```\n"

    # backend/endpoints/auth.py
    python_files += "### `backend/endpoints/auth.py`\n**Login/Logout Routes**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/endpoints/auth.py", "@router.post(\"/login\")", max_lines=100)
    python_files += "\n```\n"

    # backend/endpoints/html_routes.py (full content)
    python_files += "### `backend/endpoints/html_routes.py`\n**HTML Routes (Full Content)**\n```python\n"
    python_files += get_full_file_content(repo_path / "backend/endpoints/html_routes.py")
    python_files += "\n```\n"

    # backend/endpoints/lookups.py (full content)
    python_files += "### `backend/endpoints/lookups.py`\n**Lookup Endpoints (Full Content)**\n```python\n"
    python_files += get_full_file_content(repo_path / "backend/endpoints/lookups.py")
    python_files += "\n```\n"

    # backend/endpoints/orders.py (full content)
    python_files += "### `backend/endpoints/orders.py`\n**Order Management Endpoints (Full Content)**\n```python\n"
    python_files += get_full_file_content(repo_path / "backend/endpoints/orders.py")
    python_files += "\n```\n"

    # backend/endpoints/requesters.py
    python_files += "### `backend/endpoints/requesters.py`\n**Requester Endpoints**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/endpoints/requesters.py", "@router", max_lines=100)
    python_files += "\n```\n"

    # backend/endpoints/supplier_lookup.py
    python_files += "### `backend/endpoints/supplier_lookup.py`\n**Supplier Lookup Endpoints**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/endpoints/supplier_lookup.py", "@router", max_lines=100)
    python_files += "\n```\n"

    # backend/endpoints/supplier_lookup_takealot.py
    python_files += "### `backend/endpoints/supplier_lookup_takealot.py`\n**Takealot Supplier Lookup**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/endpoints/supplier_lookup_takealot.py", "@router", max_lines=100)
    python_files += "\n```\n"

    # backend/twilio/twilio_utils.py (full content)
    python_files += "### `backend/twilio/twilio_utils.py`\n**WhatsApp Notifications (Full Content)**\n```python\n"
    python_files += get_full_file_content(repo_path / "backend/twilio/twilio_utils.py")
    python_files += "\n```\n"

    # backend/utils/order_utils.py
    python_files += "### `backend/utils/order_utils.py`\n**Order Utilities**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/utils/order_utils.py", "def", max_lines=100)
    python_files += "\n```\n"

    # backend/main.py
    python_files += "### `backend/main.py`\n**FastAPI Application Setup**\n```python\n"
    python_files += get_file_snippet(repo_path / "backend/main.py", max_lines=100)
    python_files += "\n```\n"

    # data/orders.py
    python_files += "### `data/orders.py`\n**Order Data Logic**\n```python\n"
    python_files += get_file_snippet(repo_path / "data/orders.py", max_lines=100)
    python_files += "\n```\n"

    # Database Schema
    db_schema = "## 🗄️ Database Schema (`data/orders.db`)\n_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._\n"
    db_schema += get_database_schema(db_path)

    # Frontend Overview
    frontend = "## 🌐 Frontend Overview\n"

    # HTML Templates
    frontend += "### HTML Templates (`frontend/templates/`)\n"
    for html_file in (repo_path / "frontend/templates").glob("*.html"):
        frontend += f"\n#### `{html_file.name}`\n```html\n"
        frontend += get_file_snippet(html_file, max_lines=100)
        frontend += "\n```\n"

    # JavaScript Files
    frontend += "\n### JavaScript (`frontend/static/js/`)\n"
    for js_file in (repo_path / "frontend/static/js").glob("*.js"):
        frontend += f"\n#### `{js_file.name}`\n```javascript\n"
        if js_file.name in ["pending_orders.js", "received_orders.js"]:
            frontend += get_full_file_content(js_file)
        else:
            frontend += get_file_snippet(js_file, max_lines=100)
        frontend += "\n```\n"

    # JavaScript Components
    frontend += "\n### Components (`frontend/static/js/components/`)\n"
    for js_file in (repo_path / "frontend/static/js/components").glob("*.js"):
        frontend += f"\n#### `{js_file.name}`\n```javascript\n"
        frontend += get_file_snippet(js_file, max_lines=100)
        frontend += "\n```\n"

    # Environment Variables (.env)
    env_vars = "## 🌍 Environment Variables (`.env`)\n```plaintext\n"
    env_vars += get_file_snippet(env_path, max_lines=100)
    env_vars += "\n```\n"

    # Dependencies (requirements.txt)
    dependencies = "## 📦 Dependencies (`requirements.txt`)\n```plaintext\n"
    dependencies += get_file_snippet(repo_path / "requirements.txt", max_lines=100)
    dependencies += "\n```\n"

    # Logs Overview
    logs = "## 📜 Logs Overview\n"
    log_files = [
        "db_activity_log.txt",
        "lookups_log.txt",
        "message_sid_mapping.json",
        "new_orders_log.txt",
        "phone_order_mapping.json",
        "server.log",
        "supplier_lookup_debug.log",
        "takealot_lookup.log",
        "testing_log.txt",
        "twilio.log",
        "whatsapp_log.txt"
    ]
    for log_file in log_files:
        log_path = repo_path / "logs" / log_file
        logs += f"\n### `{log_file}`\n**Recent Entries (Last 20 Lines)**\n```plaintext\n"
        logs += get_log_snippet(log_path, max_lines=20)
        logs += "\n```\n"

    # Users & Roles
    users_roles = """## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

"""

    # System Settings
    settings = """## ⚙️ System Settings

| Key                 | Value   |
|---------------------|---------|
| auth_threshold      | 10000   |
| order_number_start  | URC1024 |
| last_order_number   | URC000  |

"""

    # FastAPI Endpoint Summary
    endpoints = """## 🚦 FastAPI Endpoint Summary

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

    # Test Coverage Summary
    test_coverage = """## 🧪 Test Coverage Summary

| Test Script | Purpose | Status |
|-------------|---------|--------|
| `test_authorisation_threshold_trigger.py` | High-value order triggers auth flow | ✅ |
| `test_invalid_data_handling.py` | Ensures invalid payloads return 422/400 | ✅ |
| `test_invalid_items_variants.py` | Covers malformed line item edge cases | ✅ |
| `test_pipeline_end_to_end.py` | Full pipeline test: creation → receive | ✅ |
| `test_receive_partial.py` | Tests partial receiving with audit tracking | ✅ |

"""

    # TODOs
    todos = """## ✅ TODOs (Static Manual Items)

- [ ] Modularize long `.js` files into reusable components
- [ ] Finalize `/audit` route with filters + trail UI
- [ ] Finalize `/orders/print` layout + backend
- [ ] Add RBAC (role-based access control)
- [ ] Pagination on long tables (Pending/Received)
- [ ] Security audit on file uploads
- [ ] Normalize filenames and harden upload paths
- [ ] Add upload success/failure status to frontend

"""

    # Combine all sections
    full_content = f"{intro}\n{dir_structure}\n{python_files}\n{db_schema}\n{frontend}\n{env_vars}\n{dependencies}\n{logs}\n{users_roles}\n{settings}\n{endpoints}\n{test_coverage}\n{todos}"

    # Write to project_summary.md
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ Generated {output_file}")

if __name__ == "__main__":
    main()