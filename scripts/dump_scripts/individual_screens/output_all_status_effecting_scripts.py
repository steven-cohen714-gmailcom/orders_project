#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from pathlib import Path
import sqlite3

valid_extensions = {'.py', '.html', '.js', '.css', '.txt', '.json'}

# --- CONFIG ---
project_root = Path('/Users/stevencohen/Projects/universal_recycling/orders_project')
output_dir = Path.home() / 'Desktop'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = output_dir / f'status_affecting_scripts_dump_{timestamp}.txt'

# --- FILES TO INCLUDE ---
focused_files_set = {
    # Core backend
    project_root / 'backend' / 'main.py',
    project_root / 'backend' / 'database.py',
    project_root / 'backend' / 'endpoints' / 'orders.py',
    project_root / 'backend' / 'endpoints' / 'lookups / mark_cod_paid_api.py',
    
    # Frontend scripts that affect status
    project_root / 'frontend' / 'static' / 'js' / 'new_order_screen' / 'submit_utils.js',
    project_root / 'frontend' / 'static' / 'js' / 'components' / 'receive_modal.js',
    project_root / 'frontend' / 'static' / 'js' / 'components' / 'payments_modal.js',
    project_root / 'frontend' / 'static' / 'js' / 'partially_delivered.js',

}

focused_files = sorted(list(focused_files_set))

# --- OUTPUT START ---
output_dir.mkdir(exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the directory tree
    try:
        tree_output = subprocess.check_output(['tree', '-L', '4', str(project_root)], text=True)
        output_file.write("DIRECTORY TREE:\n")
        output_file.write(tree_output)
    except FileNotFoundError:
        output_file.write("DIRECTORY TREE (Fallback - 'tree' command not found):\n")
        for dirpath, dirnames, filenames in os.walk(project_root):
            level = dirpath.replace(str(project_root), '').count(os.sep)
            indent = ' ' * 4 * level
            output_file.write(f"{indent}{os.path.basename(dirpath)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for f in filenames:
                output_file.write(f"{subindent}{f}\n")
    output_file.write("\n" + "=" * 80 + "\n")

    # Write the database schema
    db_path = project_root / 'data' / 'orders.db'
    try:
        conn = sqlite3.connect(str(db_path))
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

    # Dump each script
    for file_path in focused_files:
        relative_path = file_path.relative_to(project_root)

        if not file_path.exists() or file_path.suffix.lower() not in valid_extensions:
            output_file.write(f"FILE: {relative_path}\n")
            output_file.write(f"❌ Skipped or not found: {relative_path}\n")
            output_file.write(f"END OF FILE: {relative_path}\n")
            output_file.write("=" * 80 + "\n")
            continue

        output_file.write(f"FILE: {relative_path}\n")
        try:
            with open(file_path, 'r', encoding='utf-8') as src:
                content = src.read()
                output_file.write(content)
        except Exception as e:
            output_file.write(f"❌ Error reading file: {relative_path} - {str(e)}\n")
        output_file.write(f"\nEND OF FILE: {relative_path}\n")
        output_file.write("=" * 80 + "\n")

print(f"✅ Done. Full output at: {output_file_path}")
