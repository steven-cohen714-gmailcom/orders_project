from pathlib import Path
import os
import sqlite3
import subprocess

os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_maintenance_screen_files.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in [
        "frontend/static/css/style.css",
        "backend/endpoints/html_routes.py",
        "backend/endpoints/lookups/settings.py",
        "backend/endpoints/lookups/users.py",
        "backend/endpoints/lookups/items.py",
        "backend/endpoints/lookups/suppliers.py",
        "backend/endpoints/lookups/projects.py",
        "backend/endpoints/lookups/requesters.py",
        "backend/endpoints/lookups/requisitioners.py",
        "backend/endpoints/utils.py",
        "backend/database.py",
        "backend/main.py",
        "frontend/templates/maintenance.html",
        "frontend/static/js/maintenance_screen/users.js",  
        "frontend/static/js/maintenance_screen/requesters.js",  
        "frontend/static/js/maintenance_screen/items.js",  
        "frontend/static/js/maintenance_screen/suppliers.js",  
        "frontend/static/js/maintenance_screen/projects.js",  
        "frontend/static/js/maintenance_screen/settings.js",  
        "frontend/static/js/maintenance_screen/business_details.js",  
        "frontend/static/js/maintenance_screen/index.js",  
        "frontend/static/js/maintenance.js",  
    ]:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")

    # --- Append DB Schema ---
    f.write("📦 DATABASE SCHEMA: data/orders.db\n" + "="*60 + "\n")
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for (table_name,) in tables:
            f.write(f"\n🔸 Table: {table_name}\n")
            cursor.execute(f"PRAGMA table_info({table_name});")
            for col in cursor.fetchall():
                f.write(f"  {col[1]} ({col[2]})\n")
        conn.close()
    except Exception as e:
        f.write(f"[ERROR] Could not read database schema: {e}\n")

    # --- Append Tree Output ---
    f.write("\n🌲 PROJECT TREE (depth=4)\n" + "="*60 + "\n")
    try:
        tree_output = subprocess.run(["tree", "-L", "4"], capture_output=True, text=True)
        f.write(tree_output.stdout)
    except FileNotFoundError:
        f.write("[ERROR] 'tree' command not found. Try 'brew install tree' or 'apt install tree'\n")
