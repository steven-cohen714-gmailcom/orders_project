#!/usr/bin/env python3

import os
import subprocess
import sqlite3

# Define root project directory
root_dir = '/Users/stevencohen/Projects/universal_recycling/orders_project'

# Only include these subdirectories
include_dirs = {'backend', 'frontend'}

# Define output file path
output_dir = '/Users/stevencohen/Desktop'
output_file_path = os.path.join(output_dir, 'entire_project_dump.txt')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the directory tree
    try:
        tree_output = subprocess.check_output(['tree', '-L', '4', root_dir], text=True)
        output_file.write("DIRECTORY TREE:\n")
        output_file.write(tree_output)
        output_file.write("\n" + "=" * 80 + "\n")
    except subprocess.CalledProcessError as e:
        output_file.write(f"Error generating directory tree: {e}\n")
        output_file.write("=" * 80 + "\n")

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
    except sqlite3.Error as e:
        output_file.write(f"Error retrieving database schema: {e}\n")
        output_file.write("=" * 80 + "\n")

    # Traverse only backend/ and frontend/
    for subdir in include_dirs:
        target_path = os.path.join(root_dir, subdir)
        for dirpath, dirnames, filenames in os.walk(target_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                output_file.write(f"FILE: {file_path}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        output_file.write(content)
                except UnicodeDecodeError:
                    output_file.write(f"❌ Could not decode file as UTF-8: {file_path}\n")
                except Exception as e:
                    output_file.write(f"❌ Error reading file: {file_path} - {str(e)}\n")
                output_file.write(f"\nEND OF FILE: {file_path}\n")
                output_file.write("=" * 80 + "\n")
