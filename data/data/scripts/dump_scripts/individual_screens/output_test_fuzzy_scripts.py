from pathlib import Path
import os
import sqlite3
import subprocess

# --- Setup ---
os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_test_items_dropdown.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

# --- Files involved in test_items_dropdown ---
test_fuzzy_dropdown_files = [
    # 🔧 Test backend (mock or simplified lookup endpoints)
    "test_items_dropdown/backend/test_items_lookup.py",

    # 🧠 Standalone fuzzy dropdown logic under test
    "test_items_dropdown/frontend/static/js/fuzzy_dropdown_test.js",

    # 🧾 Test HTML file to render dropdown
    "test_items_dropdown/frontend/templates/test_dropdown_screen.html",

    # 📚 Utilities if used
    "test_items_dropdown/frontend/static/js/utils_test.js",

    # 🎨 Optional: styling
    "test_items_dropdown/frontend/static/css/test_style.css",
]

# --- Output all relevant file contents ---
with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in test_fuzzy_dropdown_files:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")

    # --- DB schema (optional, comment out if not used in test setup) ---
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

    # --- Tree view of the test directory ---
    f.write("\n🌲 TEST DIRECTORY TREE (depth=5)\n" + "="*60 + "\n")
    try:
        tree_output = subprocess.run(["tree", "test_items_dropdown", "-L", "5"], capture_output=True, text=True)
        f.write(tree_output.stdout)
    except Exception:
        f.write("[ERROR] 'tree' command not found. Try 'brew install tree'\n")
