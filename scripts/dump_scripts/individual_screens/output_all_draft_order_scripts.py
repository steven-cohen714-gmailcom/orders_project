#scripts/dump_scripts/individual_screens/output_all_draft_order_scripts.py

#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from pathlib import Path
import sqlite3

valid_extensions = {'.py', '.html', '.js', '.css', '.txt', '.json'}

# Define root project directory and output location
project_root = Path('/Users/stevencohen/Projects/universal_recycling/orders_project')
output_dir = Path.home() / 'Desktop'

# Define focused files. Using a set initially handles duplicates automatically.
focused_files_set = {
    # Core files that affect the entire application
    project_root / 'backend' / 'main.py',
    project_root / 'backend' / 'database.py',
    project_root / 'backend' / 'endpoints' / 'orders.py',
    project_root / 'backend' / 'endpoints' / 'auth.py',
    project_root / 'backend' / 'utils' / 'permissions_utils.py',
    project_root / 'frontend' / 'templates' / '_tab_nav.html',
    project_root / 'frontend' / 'static' / 'css' / 'style.css',
    project_root / 'frontend' / 'static' / 'css' / 'core-ui.css',
    project_root / 'frontend' / 'static' / 'js' / 'components' / 'utils.js',
    
    # Files directly related to the draft order workflow
    project_root / 'backend' / 'endpoints' / 'draft_orders.py',
    project_root / 'frontend' / 'templates' / 'draft_orders.html',
    project_root / 'frontend' / 'static' / 'js' / 'draft_orders_main.js',
    project_root / 'frontend' / 'templates' / 'new_order.html',
    project_root / 'frontend' / 'static' / 'js' / 'new_order_main.js',
    project_root / 'frontend' / 'static' / 'js' / 'new_order_screen' / 'submit_utils.js',
    project_root / 'frontend' / 'static' / 'js' / 'new_order_screen' / 'submit_draft_order_utils.js',
    project_root / 'scripts' / 'database_scripts' / 'clear_dynamic_database_tables.py',
}

# Add some other key files that might be relevant to the flow
additional_relevant_files = {
    project_root / 'backend' / 'endpoints' / 'order_queries.py',
    project_root / 'backend' / 'endpoints' / 'lookups' / 'settings.py',
    project_root / 'frontend' / 'static' / 'js' / 'components' / 'fuzzy_dropdown.js',
    project_root / 'frontend' / 'static' / 'js' / 'components' / 'pdf_modal.js',
    project_root / 'frontend' / 'static' / 'js' / 'components' / 'attachment_modal.js',
    project_root / 'frontend' / 'static' / 'js' / 'pending_orders.js',
}
focused_files_set.update(additional_relevant_files)

# Sort the final list of files for consistent output.
focused_files = sorted(list(focused_files_set))

# Define output file path
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = output_dir / f'draft_orders_focused_dump_{timestamp}.txt'

# Ensure output directory exists
output_dir.mkdir(exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the directory tree (with fallback)
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
    except Exception as e:
        output_file.write(f"Error generating directory tree: {e}\n")
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

    # Dump focused files
    for file_path in focused_files:
        relative_path = file_path.relative_to(project_root)
        
        # Check if the file exists and is a text file before trying to read it
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
                # Use a smaller limit for focused dumps
                max_size = 500 * 1024 # 500KB
                if len(content.encode('utf-8')) > max_size:
                    output_file.write(f"⚠️ File too large (>500KB), first 1000 chars shown:\n")
                    output_file.write(content[:1000] + "\n[...TRUNCATED...]\n")
                else:
                    output_file.write(content)
        except Exception as e:
            output_file.write(f"❌ Error reading file: {relative_path} - {str(e)}\n")
        output_file.write(f"\nEND OF FILE: {relative_path}\n")
        output_file.write("=" * 80 + "\n")

    print(f"✅ Script generated. Output file: {output_file_path}")