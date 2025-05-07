import os
import shutil
import sqlite3
import subprocess
import logging

# --- Config ---
PROJECT_ROOT = "/Users/stevencohen/Projects/universal_recycling/orders_project"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "scripts_for_entire_project")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "scripts_for_entire_project.txt")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "orders.db")
TARGET_DIRS = ["backend", "frontend"]

# --- Setup Logging ---
logging.basicConfig(
    filename=os.path.join(PROJECT_ROOT, "logs", "snapshot_errors.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

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
        logging.error(f"Tree command failed: {str(e)}")

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
        logging.error(f"Pip list failed: {str(e)}")

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
            logging.error(f"DB schema read failed: {str(e)}")
    else:
        out_file.write("[orders.db not found]\n")
        logging.warning("orders.db not found")

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
        logging.info(f"Starting traversal of directory: {target_path}")
        for root, dirs, files in os.walk(target_path):
            # Skip __pycache__ directories
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            # Sort directories and files for consistent output
            dirs.sort()
            files.sort()
            logging.info(f"Processing directory: {root} with files: {files}")
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, PROJECT_ROOT)
                logging.info(f"Attempting to process file: {full_path}")
                try:
                    if not os.path.isfile(full_path):
                        logging.error(f"File does not exist or is not a file: {full_path}")
                        out_file.write(f"\n\n[ERROR reading file: {full_path}] - File does not exist or is not a file\n")
                        continue
                    file_size = os.path.getsize(full_path)
                    if file_size == 0:
                        logging.warning(f"Empty file: {full_path}")
                        out_file.write(f"\n\n{'='*80}\n")
                        out_file.write(f"FILE: {relative_path}\n")
                        out_file.write(f"{'-'*80}\n")
                        out_file.write("[FILE IS EMPTY]\n")
                        continue
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    logging.info(f"Successfully read file: {full_path} ({file_size} bytes)")
                    out_file.write(f"\n\n{'='*80}\n")
                    out_file.write(f"FILE: {relative_path}\n")
                    out_file.write(f"{'-'*80}\n")
                    out_file.write(content)
                except UnicodeDecodeError as e:
                    logging.error(f"Unicode decode error for file {full_path}: {str(e)}")
                    out_file.write(f"\n\n[ERROR reading file: {full_path}] - Unicode decode error: {str(e)}\n")
                except PermissionError as e:
                    logging.error(f"Permission denied for file {full_path}: {str(e)}")
                    out_file.write(f"\n\n[ERROR reading file: {full_path}] - Permission denied: {str(e)}\n")
                except Exception as e:
                    logging.error(f"Unexpected error reading file {full_path}: {str(e)}")
                    out_file.write(f"\n\n[ERROR reading file: {full_path}] - Unexpected error: {str(e)}\n")
                finally:
                    logging.info(f"Finished processing file: {full_path}")
        logging.info(f"Completed traversal of directory: {target_path}")

    # --- Step 4: Explicitly check frontend/static/js/ ---
    js_path = os.path.join(PROJECT_ROOT, "frontend", "static", "js")
    logging.info(f"Explicitly checking directory: {js_path}")
    if os.path.isdir(js_path):
        js_files = sorted([f for f in os.listdir(js_path) if os.path.isfile(os.path.join(js_path, f))])
        logging.info(f"Files in {js_path}: {js_files}")
        for file in js_files:
            full_path = os.path.join(js_path, file)
            relative_path = os.path.relpath(full_path, PROJECT_ROOT)
            logging.info(f"Attempting to process file (explicit check): {full_path}")
            try:
                if not os.path.isfile(full_path):
                    logging.error(f"File does not exist or is not a file: {full_path}")
                    out_file.write(f"\n\n[ERROR reading file: {full_path}] - File does not exist or is not a file\n")
                    continue
                file_size = os.path.getsize(full_path)
                if file_size == 0:
                    logging.warning(f"Empty file: {full_path}")
                    out_file.write(f"\n\n{'='*80}\n")
                    out_file.write(f"FILE: {relative_path}\n")
                    out_file.write(f"{'-'*80}\n")
                    out_file.write("[FILE IS EMPTY]\n")
                    continue
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                logging.info(f"Successfully read file (explicit check): {full_path} ({file_size} bytes)")
                out_file.write(f"\n\n{'='*80}\n")
                out_file.write(f"FILE: {relative_path}\n")
                out_file.write(f"{'-'*80}\n")
                out_file.write(content)
            except UnicodeDecodeError as e:
                logging.error(f"Unicode decode error for file {full_path}: {str(e)}")
                out_file.write(f"\n\n[ERROR reading file: {full_path}] - Unicode decode error: {str(e)}\n")
            except PermissionError as e:
                logging.error(f"Permission denied for file {full_path}: {str(e)}")
                out_file.write(f"\n\n[ERROR reading file: {full_path}] - Permission denied: {str(e)}\n")
            except Exception as e:
                logging.error(f"Unexpected error reading file {full_path}: {str(e)}")
                out_file.write(f"\n\n[ERROR reading file: {full_path}] - Unexpected error: {str(e)}\n")
            finally:
                logging.info(f"Finished processing file (explicit check): {full_path}")
    else:
        logging.error(f"Directory does not exist: {js_path}")
        out_file.write(f"\n\n[ERROR: Directory does not exist: {js_path}]\n")

print(f"✅ Done. Output written to: {OUTPUT_FILE}")