#!/usr/bin/env python3
import os
import sqlite3
from pathlib import Path
import hashlib
import logging
import sys
import time

# --- Config ---
PROJECT_ROOT = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
OUTPUT_FILE = PROJECT_ROOT / "output_received_order_screen_files.md"
DB_FILE = PROJECT_ROOT / "data/orders.db"
LOG_FILE = PROJECT_ROOT / "logs/output_received_order_screen_files.log"

FILES_TO_DUMP = [
    "frontend/templates/received_orders.html",
    "frontend/static/js/received_orders.js",
    "frontend/static/js/components/expand_line_items.js",
    "frontend/static/js/components/attachment_modal.js",
    "frontend/static/js/components/order_note_modal.js",
    "frontend/static/js/components/shared_filters.js",
    "backend/main.py",
    "backend/endpoints/html_routes.py",
    "backend/endpoints/orders.py",
    "backend/endpoints/lookups.py",
    "backend/endpoints/order_queries.py",
    "backend/endpoints/order_attachments.py",
    "backend/endpoints/order_notes.py",
    "backend/database.py"
]

# --- Setup logging ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

missed_files = []

def get_file_hash(file_path):
    try:
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        logging.error(f"Failed to hash {file_path}: {e}")
        return None

def get_file_mtime(file_path):
    try:
        mtime = os.path.getmtime(file_path)
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    except Exception as e:
        logging.error(f"Failed to get mtime for {file_path}: {e}")
        return "Unknown"

def get_database_schema():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        schema = [
            f"### Table: {name}\n```sql\n{sql}\n```"
            for name, sql in cursor.fetchall()
        ]
        conn.close()
        return "\n\n".join(schema) if schema else "No tables found in database."
    except sqlite3.Error as e:
        logging.error(f"Error accessing database schema: {e}")
        return f"Error accessing database schema: {e}"

def main():
    print("🛠 Dumping Received Orders Screen files...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("# Received Orders Screen Files\n\n")
            f.write("Generated for focused screen development.\n\n")

            f.write("## File Contents\n")

            for rel_path in FILES_TO_DUMP:
                file_path = PROJECT_ROOT / rel_path
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as src:
                            content = src.read()

                        file_hash = get_file_hash(file_path)
                        file_mtime = get_file_mtime(file_path)
                        ext = file_path.suffix[1:] if file_path.suffix.startswith('.') else 'txt'

                        f.write(f"### File: {rel_path}\n")
                        f.write(f"**SHA-256 Hash**: {file_hash}\n\n")
                        f.write(f"**Last Modified**: {file_mtime}\n\n")
                        f.write(f"```{ext}\n{content}\n```\n\n")

                        logging.info(f"✅ Dumped {rel_path}")

                    except Exception as e:
                        missed_files.append(str(rel_path))
                        logging.error(f"❌ Error reading {rel_path}: {e}")
                        f.write(f"### File: {rel_path}\n(Error reading file: {e})\n\n")
                else:
                    missed_files.append(str(rel_path))
                    logging.error(f"❌ Missing file: {rel_path}")
                    f.write(f"### File: {rel_path}\n(File not found)\n\n")

            # Database Schema
            f.write("## Database Schema\n")
            f.write(get_database_schema())
            f.write("\n")

        if missed_files:
            print("\n❌ The following files were missing or could not be read:")
            for file in missed_files:
                print(f"- {file}")
            sys.exit(1)
        else:
            print("\n✅ All Received Orders screen files successfully dumped.")
            sys.exit(0)

    except Exception as e:
        logging.error(f"Fatal error during dump: {e}")
        print(f"❌ Fatal error. See {LOG_FILE} for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
