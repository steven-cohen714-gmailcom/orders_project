#!/usr/bin/env python3

from pathlib import Path
import os
import sqlite3
import subprocess

# --- Setup ---
os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_cod_screen.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

# --- COD-Specific Files ---
cod_files = [
    # COD backend API
    "backend/endpoints/orders/cod_orders_api.py",
    "backend/endpoints/orders/mark_cod_paid_api.py",
    
    # COD frontend HTML and JS
    "frontend/templates/cod_payments_screen.html",
    "frontend/static/js/cod_payments_screen.js",
]

# --- Write file contents ---
with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in cod_files:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")

    # --- COD-relevant DB schema fields ---
    f.write("📦 COD-RELATED DATABASE FIELDS\n" + "="*60 + "\n")
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()

        f.write("\n🔸 Table: orders\n")
        cursor.execute("PRAGMA table_info(orders);")
        for col in cursor.fetchall():
            if "payment" in col[1].lower():
                f.write(f"  {col[1]} ({col[2]})\n")

        conn.close()
    except Exception as e:
        f.write(f"[ERROR] Could not read database schema: {e}\n")

    # --- Optional: append partial tree for reference ---
    f.write("\n🌲 PROJECT TREE (depth=3)\n" + "="*60 + "\n")
    try:
        tree_output = subprocess.run(["tree", "-L", "3"], capture_output=True, text=True)
        f.write(tree_output.stdout)
    except FileNotFoundError:
        f.write("[ERROR] 'tree' command not found. Try 'brew install tree' or 'apt install tree'\n")
