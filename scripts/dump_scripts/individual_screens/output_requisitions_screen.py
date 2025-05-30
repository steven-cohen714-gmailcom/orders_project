from pathlib import Path
import os
import sqlite3
import subprocess

# --- Setup ---
os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_requisitions_screen.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

# --- All relevant files impacting Requisitions ---
requisition_feature_files = [
    # 🔧 Backend entry & DB
    "backend/main.py",
    "backend/database.py",

    # 📦 Requisition-related API logic
    "backend/endpoints/orders/order_queries.py",
    "backend/endpoints/requisitions.py",  # assumed file

    # 🔐 Auth & Permissions enforcement
    "backend/endpoints/auth.py",
    "backend/endpoints/html_routes.py",
    "backend/utils/permissions_utils.py",

    # 🧑‍💼 Users / Role DB mapping
    "backend/endpoints/lookups/users.py",
    "frontend/templates/access_denied.html",

    # 🖥️ Requisition Screen
    "frontend/templates/pending_requisitions.html",
    "frontend/static/js/pending_requisitions.js",
    "frontend/static/js/requisition_modal.js",  # optional

    # 🌐 Shared UI/UX dependencies
    "frontend/static/js/components/shared_filters.js",
    "frontend/static/js/components/pdf_modal.js",
    "frontend/static/js/components/utils.js",

    # 📐 Styling
    "frontend/static/css/style.css",

    # 🧪 Other affected screens
    "frontend/static/js/maintenance.js",
    "frontend/templates/maintenance.html",
    "frontend/static/js/authorisations_per_user.js",
]

# --- Output all relevant file contents ---
with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in requisition_feature_files:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")

    # --- DB schema ---
    f.write("📦 DATABASE SCHEMA: data/orders.db\n" + "="*60 + "\n")
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
    f.write("\n🌲 PROJECT TREE (depth=5)\n" + "="*60 + "\n")
    try:
        tree_output = subprocess.run(["tree", "-L", "5"], capture_output=True, text=True)
        f.write(tree_output.stdout)
    except Exception:
        f.write("[ERROR] 'tree' command not found. Try 'brew install tree'\n")
