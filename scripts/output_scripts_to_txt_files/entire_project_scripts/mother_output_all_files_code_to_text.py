import os
import shutil
import sqlite3
import subprocess

# --- Config ---
PROJECT_ROOT = "/Users/stevencohen/Projects/universal_recycling/orders_project"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "scripts_for_entire_project")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "scripts_for_entire_project.txt")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "orders.db")
TARGET_DIRS = ["backend", "frontend"]
INCLUDED_EXTENSIONS = {".py", ".js", ".html", ".css"}

# --- Step 1: Recreate Output Directory ---
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

# --- Step 2: Write tree, pip list, db schema ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:

    # Tree
    out_file.write("TREE STRUCTURE (Level 5)\n")
    out_file.write("=" * 80 + "\n")
    try:
        tree_output = subprocess.check_output(["tree", "-L", "5", PROJECT_ROOT], text=True)
        out_file.write(tree_output)
    except Exception as e:
        out_file.write(f"[ERROR: Could not run tree command] - {str(e)}\n")

    # Dependencies
    out_file.write("\n\nINSTALLED DEPENDENCIES (pip list)\n")
    out_file.write("=" * 80 + "\n")
    try:
        pip_output = subprocess.check_output([
            os.path.join(PROJECT_ROOT, "venv", "bin", "pip"), "list"
        ], text=True)
        out_file.write(pip_output)
    except Exception as e:
        out_file.write(f"[ERROR: Could not list pip packages] - {str(e)}\n")

    # DB Schema
    out_file.write("\n\nDATABASE SCHEMA: orders.db\n")
    out_file.write("=" * 80 + "\n")
    if os.path.exists(DB_PATH):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    out_file.write(f"\n--- Table: {table[0]} ---\n")
                    cursor.execute(f"PRAGMA table_info({table[0]});")
                    cols = cursor.fetchall()
                    for col in cols:
                        out_file.write(f"{col}\n")
        except Exception as e:
            out_file.write(f"[ERROR reading DB schema] - {str(e)}\n")
    else:
        out_file.write("[orders.db not found]\n")

            # Table Usage Summary
    out_file.write("\n\nTABLE USAGE SUMMARY\n")
    out_file.write("=" * 80 + "\n")
    out_file.write("""
Table             | Static? | Used In Screens
------------------|---------|--------------------------------------------------------------
attachments        |         | audit_trail, new_order, pending_orders, received_orders
audit_trail        |         | audit_trail, new_order, received_orders
business_details   | ✅      | maintenance, new_order
items              | ✅      | maintenance, new_order
order_items        |         | new_order, pending_orders, received_orders
orders             |         | new_order, pending_orders, received_orders, audit_trail
projects           | ✅      | maintenance, new_order
requesters         | ✅      | maintenance, new_order, pending_orders
settings           | ✅      | maintenance, new_order
suppliers          | ✅      | maintenance, new_order, pending_orders
users              | ✅      | home, login, maintenance
""")

    # Spacer
    out_file.write("\n\nPROJECT CODE FILES\n")
    out_file.write("=" * 80 + "\n")

    # --- Step 3: Collect code files ---
    for base in TARGET_DIRS:
        target_path = os.path.join(PROJECT_ROOT, base)
        for root, dirs, files in os.walk(target_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in INCLUDED_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        relative_path = os.path.relpath(full_path, PROJECT_ROOT)
                        out_file.write(f"\n\n{'='*80}\n")
                        out_file.write(f"FILE: {relative_path}\n")
                        out_file.write(f"{'-'*80}\n")
                        out_file.write(content)
                    except Exception as e:
                        out_file.write(f"\n\n[ERROR reading file: {full_path}] - {str(e)}")

print(f"✅ Done. Output written to: {OUTPUT_FILE}")
