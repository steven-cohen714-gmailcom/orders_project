from pathlib import Path
import os
import sqlite3
import subprocess

# --- Setup ---
os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_pending_screen.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

# --- All relevant files impacting Pending Orders screen ---
pending_feature_files = [
    # 🔧 Backend entry & DB
    "backend/main.py",
    "backend/database.py",

    # 📦 Related API logic
    "backend/endpoints/orders/order_queries.py",
    "backend/endpoints/orders.py",

    # 🚀 Submission logic
    "frontend/static/js/new_order_screen/submit_utils.js",
    "frontend/static/js/new_order_main.js",

    # 📄 HTML Template
    "frontend/templates/new_order.html",

    # 🔐 Auth & Permissions enforcement
    "backend/endpoints/auth.py",
    "backend/endpoints/html_routes.py",
    "backend/utils/permissions_utils.py",

    # 👤 Users / Role DB mapping
    "backend/endpoints/lookups/users.py",
    "frontend/templates/access_denied.html",

    # 🖥️ Pending Orders Screen
    "frontend/static/js/pending_orders.js",
    "frontend/templates/pending_orders.html",

    # 🌐 Shared UI/UX dependencies
    "frontend/static/js/components/shared_filters.js",
    "frontend/static/js/components/pdf_modal.js",
    "frontend/static/js/components/utils.js",

    # 🎨 Styling
    "frontend/static/css/style.css",

    # 🧪 Other affected screens
    "frontend/static/js/maintenance.js",
    "frontend/templates/maintenance.html",
    "frontend/static/js/authorisations_per_user.js",
]

# --- Output all relevant file contents ---
with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in pending_feature_files:
        f.write(f"📄 {rel_path}\n" + "-" * 60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")

    # --- DB schema ---
    f.write("📦 DATABASE SCHEMA: data/orders.db\n" + "=" * 60 + "\n")
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for (table,) in cursor.fetchall():
            f.write(f"\n🔸 Table: {table}\n")
            cursor.execute(f"PRAGMA table_info({table});")
            for col in cursor.fetchall():
                f.write(f"  {col[1]} ({col[2]})\n")
        conn.close()
    except Exception as e:
        f.write(f"[ERROR] Could not read database schema: {e}\n")

    # --- Tree view of the project ---
    f.write("\n🌲 PROJECT TREE (depth=5)\n" + "=" * 60 + "\n")
    try:
        tree_output = subprocess.run(["tree", "-L", "5"], capture_output=True, text=True)
        f.write(tree_output.stdout)
    except Exception:
        f.write("[ERROR] 'tree' command not found. Try 'brew install tree'\n")
