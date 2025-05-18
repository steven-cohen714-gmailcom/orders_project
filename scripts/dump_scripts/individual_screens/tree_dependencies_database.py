#!/usr/bin/env python3

import os
import sqlite3
from pathlib import Path

# --- CONFIGURATION ---
project_root = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = project_root / "text_files_for_ai" / "tree_dependencies_database.txt"
database_file = project_root / "backend" / "universal_orders.db"  # Adjust if needed

# --- Generate directory tree ---
def generate_tree(path: Path, depth=4, prefix=""):
    if depth < 0 or not path.is_dir():
        return []
    result = []
    try:
        for entry in sorted(path.iterdir()):
            result.append(f"{prefix}{entry.name}")
            if entry.is_dir():
                result += generate_tree(entry, depth - 1, prefix + "    ")
    except Exception as e:
        result.append(f"{prefix}<Error: {e}>")
    return result

# --- Extract database schema ---
def extract_schema(db_path: Path):
    output = []
    if not db_path.exists():
        return ["⚠️ Database not found."]
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for (table,) in tables:
            output.append(f"\n--- Table: {table} ---")
            cursor.execute(f"PRAGMA table_info('{table}')")
            for col in cursor.fetchall():
                output.append(f"  {col[1]} ({col[2]})")
        conn.close()
    except Exception as e:
        output.append(f"⚠️ Failed to read schema: {e}")
    return output

# --- Main execution ---
if __name__ == "__main__":
    os.makedirs(output_file.parent, exist_ok=True)
    lines = ["==== Directory Tree (Level 4) ====\n"]
    lines += generate_tree(project_root, depth=4)
    lines += ["\n==== Database Schema ====\n"]
    lines += extract_schema(database_file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Output written to {output_file}")
