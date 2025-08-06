#!/usr/bin/env python3

# File: scripts/dump_scripts/entire_project_dump.py

import os
import subprocess
import sqlite3
import logging
from datetime import datetime

# Define root project directory
root_dir = '/Users/stevencohen/Projects/universal_recycling/orders_project'

# File extensions to include
# Only include the file types requested: .py, .js, and .html
valid_extensions = {'.py', '.js', '.html'}

# Define output file path with timestamp for versioning
output_dir = '/Users/stevencohen/Desktop'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = os.path.join(output_dir, f'project_dump_{timestamp}.txt')

# Setup logging
logging.basicConfig(
    filename=os.path.join(root_dir, 'logs', 'dump_script.log'),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def write_separator(file_handle, title):
    """Writes a title and separator line to the output file."""
    file_handle.write(f"\n{'=' * 80}\n")
    file_handle.write(f"--- {title} ---\n")
    file_handle.write(f"{'=' * 80}\n")
    file_handle.flush()

def dump_file_content(file_handle, file_path):
    """Safely reads and writes file content to the output."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            file_handle.write(f"\n--- FILE: {file_path} ---\n")
            file_handle.write(content)
            file_handle.write(f"\n--- END OF FILE: {file_path} ---\n")
            logging.info(f"Successfully dumped file: {file_path}")
    except Exception as e:
        file_handle.write(f"--- FAILED TO READ FILE: {file_path} ---\n")
        file_handle.write(f"Error: {e}\n")
        logging.error(f"Error reading file: {file_path} - {e}")
    finally:
        file_handle.flush()

def dump_directory_tree(file_handle):
    """Executes the tree command to generate and write the directory tree."""
    try:
        tree_output = subprocess.check_output(['tree', '-L', '4', root_dir], text=True)
        file_handle.write(tree_output)
        logging.info("Directory tree generated successfully.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        file_handle.write(f"Error generating directory tree. 'tree' command may not be installed. {e}\n")
        logging.error(f"Failed to generate directory tree: {e}")
    file_handle.flush()

def dump_db_schema(file_handle):
    """Connects to the database and writes the schema."""
    db_path = os.path.join(root_dir, 'data', 'orders.db')
    if not os.path.exists(db_path):
        file_handle.write(f"Database file not found at: {db_path}\n")
        logging.error(f"Database file not found: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        schema = cursor.fetchall()
        conn.close()
        for table in schema:
            if table[0]:
                file_handle.write(table[0] + "\n\n")
        logging.info("Database schema dumped successfully.")
    except sqlite3.Error as e:
        file_handle.write(f"Error retrieving database schema: {e}\n")
        logging.error(f"Failed to retrieve database schema: {e}")
    file_handle.flush()

# --- Main Script Execution ---
if __name__ == "__main__":
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        write_separator(output_file, "DIRECTORY TREE")
        dump_directory_tree(output_file)

        write_separator(output_file, "DATABASE SCHEMA")
        dump_db_schema(output_file)

        # Traverse the entire project directory to find all relevant files
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in sorted(filenames):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in valid_extensions:
                    file_path = os.path.join(dirpath, filename)
                    # Check if the file is within a directory that should be skipped
                    if 'logs' in dirpath or 'dump_scripts' in dirpath:
                        continue
                    dump_file_content(output_file, file_path)

    print(f"Project dump complete. Output file created at: {output_file_path}")
    logging.info("Script finished execution.")