#!/usr/bin/env python3

import os
import subprocess
import sqlite3
import logging
from datetime import datetime

# Define root project directory
root_dir = '/Users/stevencohen/Projects/universal_recycling/orders_project'

# Include these subdirectories (expanded to include scripts for debugging)
include_dirs = {'backend', 'frontend', 'scripts'}

# File extensions to include (text-based files only)
valid_extensions = {'.py', '.html', '.js', '.css', '.txt', '.json'}

# Define output file path with timestamp for versioning
output_dir = '/Users/stevencohen/Desktop'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = os.path.join(output_dir, f'entire_project_dump_{timestamp}.txt')

# Setup logging for errors and skipped files
logging.basicConfig(
    filename=os.path.join(root_dir, 'logs', 'dump_script.log'),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the directory tree
    try:
        tree_output = subprocess.check_output(['tree', '-L', '4', root_dir], text=True)
        output_file.write("DIRECTORY TREE:\n")
        output_file.write(tree_output)
        output_file.write("\n" + "=" * 80 + "\n")
        logging.info("Directory tree generated successfully.")
    except subprocess.CalledProcessError as e:
        output_file.write(f"Error generating directory tree: {e}\n")
        output_file.write("=" * 80 + "\n")
        logging.error(f"Failed to generate directory tree: {e}")

    # Write the database schema
    db_path = os.path.join(root_dir, 'data', 'orders.db')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        schema = cursor.fetchall()
        conn.close()
        output_file.write("DATABASE SCHEMA:\n")
        for table in schema:
            if table[0]:
                output_file.write(table[0] + "\n")
        output_file.write("=" * 80 + "\n")
        logging.info("Database schema dumped successfully.")
    except sqlite3.Error as e:
        output_file.write(f"Error retrieving database schema: {e}\n")
        output_file.write("=" * 80 + "\n")
        logging.error(f"Failed to retrieve database schema: {e}")

    # Traverse included directories
    for subdir in include_dirs:
        target_path = os.path.join(root_dir, subdir)
        for dirpath, dirnames, filenames in os.walk(target_path):
            for filename in sorted(filenames):  # Sort for consistent output
                file_path = os.path.join(dirpath, filename)
                # Check if file extension is valid
                if not os.path.splitext(filename)[1].lower() in valid_extensions:
                    output_file.write(f"FILE: {file_path}\n")
                    output_file.write(f"❌ Skipped non-text file (invalid extension): {file_path}\n")
                    output_file.write(f"END OF FILE: {file_path}\n")
                    output_file.write("=" * 80 + "\n")
                    logging.info(f"Skipped non-text file: {file_path}")
                    continue
                output_file.write(f"FILE: {file_path}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Optional: Limit output for very large files (e.g., >1MB)
                        max_size = 1024 * 1024  # 1MB
                        if len(content.encode('utf-8')) > max_size:
                            output_file.write(f"⚠️ File too large (>1MB), first 1000 chars shown:\n")
                            output_file.write(content[:1000] + "\n[...TRUNCATED...]\n")
                            logging.warning(f"Truncated large file: {file_path} (size: {len(content.encode('utf-8'))} bytes)")
                        else:
                            output_file.write(content)
                except UnicodeDecodeError:
                    output_file.write(f"❌ Could not decode file as UTF-8: {file_path}\n")
                    logging.error(f"Unicode decode error for file: {file_path}")
                except Exception as e:
                    output_file.write(f"❌ Error reading file: {file_path} - {str(e)}\n")
                    logging.error(f"Error reading file: {file_path} - {str(e)}", exc_info=True)
                output_file.write(f"\nEND OF FILE: {file_path}\n")
                output_file.write("=" * 80 + "\n")
                logging.info(f"Dumped file: {file_path}")