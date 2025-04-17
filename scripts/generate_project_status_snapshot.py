import os
import sqlite3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_TEMPLATES = ROOT / "frontend" / "templates"
SCRIPTS_DIR = ROOT / "scripts"
TEST_DIR = ROOT / "project_testing_scripts"
DB_PATH = ROOT / "data" / "orders.db"
OUTPUT = ROOT / "project_status_snapshot.md"

ROUTES_TO_CHECK = [
    ("/orders", "POST"),
    ("/orders/receive", "POST"),
    ("/orders/print_to_file", "GET"),
    ("/orders/print", "GET"),
    ("/orders/pending", "GET"),
    ("/orders/audit", "GET"),
    ("/orders/upload_attachment", "POST")
]

LOOKUP_TABLES = ["suppliers", "projects", "items", "requesters"]

def locate_orders_py():
    backend = ROOT / "backend"
    for path in backend.rglob("orders.py"):
        return path
    return None

def normalize(path):
    # Turns /something/{x}/more into /something
    return re.sub(r"/\{.*?\}", "", path).rstrip("/")

def extract_routes(file: Path):
    pattern = re.compile(r"@router\.(get|post|put|delete)\([\"'](.*?)[\"']\)")
    routes = []
    with file.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines(), 1):
            match = pattern.search(line)
            if match:
                method = match.group(1).upper()
                raw_path = match.group(2).strip()
                norm_path = normalize(raw_path if raw_path else "/orders")
                routes.append((method, norm_path, i, line.strip()))
    return routes

def match_route(method, expected_path, extracted_routes):
    norm_expected = normalize(expected_path)
    for m, p, line_num, code in extracted_routes:
        if m == method and p == norm_expected:
            return f"✅ Found: line {line_num}: {code}"
    return "❌ Not found"

def get_html_status():
    out = []
    if not FRONTEND_TEMPLATES.exists():
        return ["⚠️ templates folder not found"]
    for file in FRONTEND_TEMPLATES.glob("*.html"):
        size = file.stat().st_size
        out.append(f"- {file.name} → {'✅ Populated' if size > 20 else '❌ Empty'}")
    return out

def get_scripts_list():
    out = []
    if not SCRIPTS_DIR.exists():
        return ["⚠️ scripts folder missing"]
    for file in sorted(SCRIPTS_DIR.glob("*.py")):
        out.append(f"- {file.name}")
    return out

def get_tests_list():
    out = []
    if not TEST_DIR.exists():
        return ["⚠️ test directory missing"]
    for file in sorted(TEST_DIR.glob("*.py")):
        out.append(f"- {file.name}")
    return out if out else ["❌ No test scripts found"]

def lookup_table_check():
    if not DB_PATH.exists():
        return ["⚠️ Database not found — skipping lookup check"]
    out = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for table in LOOKUP_TABLES:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                out.append(f"- {table}: {'✅ Populated' if count > 0 else '❌ Empty'} ({count} rows)")
            except sqlite3.Error:
                out.append(f"- {table}: ❌ Table not found")
        conn.close()
    except sqlite3.Error as e:
        out.append(f"❌ DB error: {e}")
    return out

def main():
    lines = []
    lines.append("# 📦 Universal Recycling Orders Project Snapshot\n")

    orders_file = locate_orders_py()
    if not orders_file:
        lines.append("❌ Could not locate orders.py in /backend/")
    else:
        lines.append(f"📁 Analyzing file: {orders_file.relative_to(ROOT)}\n")
        lines.append("## 🧠 Backend Routes")
        extracted = extract_routes(orders_file)
        for route, method in ROUTES_TO_CHECK:
            match = match_route(method, route, extracted)
            lines.append(f"- {method} {route} → {match}")

    lines.append("\n## 🎨 Frontend Templates\n")
    lines.extend(get_html_status())

    lines.append("\n## ⚙️ Scripts Detected\n")
    lines.extend(get_scripts_list())

    lines.append("\n## 🧪 Test Scripts\n")
    lines.extend(get_tests_list())

    lines.append("\n## 📋 Lookup Table Check\n")
    lines.extend(lookup_table_check())

    lines.append("\n## 🗃️ Database File\n")
    lines.append(f"- {'✅ Found' if DB_PATH.exists() else '❌ Missing'} at data/orders.db")

    lines.append("\n## ✅ Summary\n")
    lines.append("- You can upload this file to a new ChatGPT session to instantly re-brief Cathy.")
    lines.append("- File generated automatically. No need to manually track dev state.\n")

    OUTPUT.write_text("\n".join(lines))
    print(f"\n✅ Snapshot created at {OUTPUT}")

if __name__ == "__main__":
    main()
