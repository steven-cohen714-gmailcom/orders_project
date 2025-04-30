#!/usr/bin/env python3
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
        return f"Error running {desc}: {e.stderr}\n"

def get_database_schema(db_path):
    print(f"Fetching database schema from {db_path}")
    schema = ""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = cursor.fetchall()
            for table_name, sql in tables:
                schema += f"Table: {table_name}\n{sql}\n\n"
    except sqlite3.Error as e:
        print(f"Error fetching schema: {e}")
        schema += f"Error fetching schema: {e}\n"
    return schema

def get_system_settings(db_path):
    print(f"Fetching system settings from {db_path}")
    settings = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings")
            settings = dict(cursor.fetchall())
    except sqlite3.Error as e:
        print(f"Error fetching settings: {e}")
        settings = {"error": str(e)}
    return settings

def get_full_file_content(file_path):
    print(f"Reading full file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            line_count = len(content.splitlines())
            return content, line_count
    except FileNotFoundError:
        return f"File not found: {file_path}\n", 1
    except Exception as e:
        return f"Error reading {file_path}: {e}\n", 1

def get_log_snippet(log_file, max_lines=20):
    print(f"Reading log file: {log_file}")
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            snippet = ''.join(lines[-max_lines:])
            line_count = len(snippet.splitlines())
            return snippet, line_count
    except FileNotFoundError:
        return f"Log file not found: {log_file}\n", 1
    except Exception as e:
        return f"Error reading {log_file}: {e}\n", 1

def ensure_log_file_exists(log_path):
    """Ensure the log file exists, creating it if necessary."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("")

def get_all_files(directory, extensions):
    """Get all files with specified extensions under the given directory."""
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f"*.{ext}"))
    return sorted(files)

def write_four_parts(output_dir, full_content):
    """Split the content into exactly four parts and write to separate files in the output directory."""
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Split the content into lines
    lines = full_content.splitlines(keepends=True)
    total_lines = len(lines)
    print(f"Total lines to split: {total_lines}")

    # Calculate lines per part (split into four parts)
    lines_per_part = total_lines // 4
    remainder = total_lines % 4

    # Adjust lines per part to distribute the remainder
    part_sizes = [lines_per_part] * 4
    for i in range(remainder):
        part_sizes[i] += 1

    print(f"Lines per part: {part_sizes}")

    # Write each part to a file
    start_idx = 0
    for part_num in range(1, 5):
        end_idx = start_idx + part_sizes[part_num - 1]
        part_lines = lines[start_idx:end_idx]
        part_content = ''.join(part_lines)
        part_file = output_dir / f"project_summary_part{part_num}.txt"
        with open(part_file, 'w', encoding='utf-8') as f:
            f.write(part_content)
        print(f"✅ Generated {part_file} ({len(part_lines)} lines)")
        start_idx = end_idx

    return 4  # Always return 4 parts

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    # Define the output directory for parts
    output_dir = repo_path / "project_summary"
    db_path = repo_path / "data/orders.db"
    env_path = repo_path / ".env"

    # Ensure pdf_generation_log.txt exists
    pdf_log_path = repo_path / "logs" / "pdf_generation_log.txt"
    ensure_log_file_exists(pdf_log_path)

    # Header
    intro = f"""Project Snapshot
================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

"""

    # Directory Tree (depth 5)
    dir_structure = """Directory Tree
----------------------------------------
"""
    dir_content = run_command(["tree", "-L", "5", str(repo_path)], "Fetching directory structure")
    dir_structure += dir_content
    dir_structure += "\n\n"
    dir_line_count = len(dir_structure.splitlines())

    # Database Schema
    db_schema = """Database Schema (`data/orders.db`)
----------------------------------------
Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs.

"""
    schema_content = get_database_schema(db_path)
    db_schema += schema_content
    db_schema += "\n\n"
    db_line_count = len(db_schema.splitlines())

    # Backend Files (dynamically include all .py files under backend/)
    backend_files = """Backend Files (`backend/`)
----------------------------------------
"""
    backend_files_list = get_all_files(repo_path / "backend", ["py"])
    backend_line_count = 0
    for file_path in backend_files_list:
        relative_path = file_path.relative_to(repo_path)
        content, line_count = get_full_file_content(file_path)
        backend_files += f"File: {relative_path}\n"
        backend_files += f"Line Count: {line_count}\n"
        backend_files += "----------------------------------------\n"
        backend_files += content
        backend_files += "\n\n----------------------------------------\n\n"
        backend_line_count += line_count + 5  # Include header lines and separators

    # Frontend Files (dynamically include all .html, .js, .css files under frontend/)
    frontend_files = """Frontend Files (`frontend/`)
----------------------------------------
"""
    frontend_files_list = get_all_files(repo_path / "frontend", ["html", "js", "css"])
    frontend_line_count = 0
    for file_path in frontend_files_list:
        relative_path = file_path.relative_to(repo_path)
        content, line_count = get_full_file_content(file_path)
        frontend_files += f"File: {relative_path}\n"
        frontend_files += f"Line Count: {line_count}\n"
        backend_files += "----------------------------------------\n"
        frontend_files += content
        frontend_files += "\n\n----------------------------------------\n\n"
        frontend_line_count += line_count + 5

    # Environment Variables (.env)
    env_vars = """Environment Variables (`.env`)
----------------------------------------
"""
    env_content, env_line_count = get_full_file_content(env_path)
    env_vars += env_content
    env_vars += "\n\n"

    # Dependencies (requirements.txt)
    dependencies = """Dependencies (`requirements.txt`)
----------------------------------------
"""
    dep_content, dep_line_count = get_full_file_content(repo_path / "requirements.txt")
    dependencies += dep_content
    dependencies += "\n\n"

    # Logs Overview
    logs = """Logs Overview
----------------------------------------
"""
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
        "whatsapp_log.txt",
        "pdf_generation_log.txt"
    ]
    logs_line_count = 0
    for log_file in log_files:
        log_path = repo_path / "logs" / log_file
        snippet, snippet_line_count = get_log_snippet(log_path, max_lines=20)
        logs += f"Log File: {log_file}\n"
        logs += "Recent Entries (Last 20 Lines)\n"
        logs += f"Line Count: {snippet_line_count}\n"
        logs += "----------------------------------------\n"
        logs += snippet
        logs += "\n\n"
        logs_line_count += snippet_line_count + 5

    # Users & Roles
    users_roles = """Users & Roles
----------------------------------------

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

"""
    users_roles_line_count = len(users_roles.splitlines())

    # System Settings
    settings_dict = get_system_settings(db_path)
    settings = """System Settings
----------------------------------------

| Key                 | Value   |
|---------------------|---------|
"""
    for key, value in settings_dict.items():
        settings += f"| {key:<19} | {value:<7} |\n"
    settings += "\n\n"
    settings_line_count = len(settings.splitlines())

    # FastAPI Endpoint Summary
    endpoints = """FastAPI Endpoint Summary
----------------------------------------

| Endpoint                     | Method    | Status         |
|------------------------------|-----------|----------------|
| `/orders`                   | POST      | ✅ Implemented |
| `/orders/receive`           | POST      | ✅ Implemented |
| `/orders/next_order_number` | GET       | ✅ Implemented |
| `/orders/upload_attachment` | POST      | ✅ Implemented |
| `/orders/attachments/{order_id}` | GET  | ✅ Implemented |
| `/orders/save_note/{order_id}` | POST | ✅ Implemented |
| `/orders/generate_pdf`      | POST      | ✅ Implemented |
| `/orders/api/orders/pending_orders` | GET | ✅ Implemented |
| `/orders/api/received_orders` | GET   | ✅ Implemented |
| `/orders/api/items_for_order/{order_id}` | GET | ✅ Implemented |
| `/orders/api/audit_trail`   | GET       | ✅ Implemented |
| `/orders/whatsapp/webhook`  | POST      | ✅ Implemented |
| `/orders/print`             | GET       | ⏳ Planned     |
| `/lookups/suppliers`        | GET       | ✅ Implemented |
| `/lookups/requesters`       | GET       | ✅ Implemented |
| `/lookups/projects`         | GET       | ✅ Implemented |
| `/lookups/items`            | GET       | ✅ Implemented |

"""
    endpoints_line_count = len(endpoints.splitlines())

    # Test Coverage Summary
    test_coverage = """Test Coverage Summary
----------------------------------------

| Test Script | Purpose | Status |
|-------------|---------|--------|
| `test_authorisation_threshold_trigger.py` | High-value order triggers auth flow | ✅ |
| `test_invalid_data_handling.py` | Ensures invalid payloads return 422/400 | ✅ |
| `test_invalid_items_variants.py` | Covers malformed line item edge cases | ✅ |
| `test_pipeline_end_to_end.py` | Full pipeline test: creation → receive | ✅ |
| `test_receive_partial.py` | Tests partial receiving with audit tracking | ✅ |

"""
    test_coverage_line_count = len(test_coverage.splitlines())

    # TODOs
    todos = """TODOs (Static Manual Items)
----------------------------------------

- [ ] Modularize long `.js` files into reusable components
- [ ] Finalize `/orders/print` layout + backend
- [ ] Add RBAC (role-based access control)
- [ ] Pagination on long tables (Pending/Received)
- [ ] Security audit on file uploads
- [ ] Normalize filenames and harden upload paths
- [ ] Add upload success/failure status to frontend

"""
    todos_line_count = len(todos.splitlines())

    # Combine all sections
    full_content = (
        intro +
        dir_structure +
        db_schema +
        backend_files +
        frontend_files +
        env_vars +
        dependencies +
        logs +
        users_roles +
        settings +
        endpoints +
        test_coverage +
        todos
    )

    # Split the content into exactly four parts and write to separate files
    total_parts = write_four_parts(output_dir, full_content)

    # Print total line count
    total_lines = (
        4 +  # Header
        dir_line_count +
        db_line_count +
        backend_line_count +
        frontend_line_count +
        env_line_count +
        dep_line_count +
        logs_line_count +
        users_roles_line_count +
        settings_line_count +
        endpoints_line_count +
        test_coverage_line_count +
        todos_line_count
    )
    print(f"Total Lines: {total_lines}")
    print(f"Total Parts Generated: {total_parts}")
    print(f"All parts have been saved in: {output_dir}")

if __name__ == "__main__":
    main()