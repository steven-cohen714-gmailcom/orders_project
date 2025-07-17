# File: generate_audit_trail_dump.py
# This script collects all files related to the Audit Trail screen and the database schema
# and outputs them to a single text file on the user's desktop.

import os
import sys
from pathlib import Path
import sqlite3
from datetime import datetime # ADDED THIS IMPORT

def get_db_schema(db_path):
    """Connects to the SQLite database and extracts its schema."""
    schema = ""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            schema += f"{table[0]};\n"
        conn.close()
    except sqlite3.Error as e:
        schema = f"Error reading database schema from {db_path}: {e}\n"
    return schema

def get_file_content(file_path):
    """Reads the content of a file, handling potential decoding errors."""
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding='latin-1') # Fallback for other encodings
        except Exception as e:
            return f"Error: Could not decode file {file_path} - {e}\n"
    except Exception as e:
        return f"Error reading file {file_path}: {e}\n"

def main():
    # Determine the project root dynamically
    # Assumes this script is run from within the project directory or its scripts/ folder
    script_path = Path(__file__).resolve()
    # Navigate up to find the project root (e.g., where backend/ and frontend/ are)
    project_root = script_path
    while not (project_root / "backend").is_dir() or not (project_root / "frontend").is_dir():
        if project_root.parent == project_root: # Reached root without finding project structure
            print("Error: Could not determine project root. Please run this script from within your project directory.")
            sys.exit(1)
        project_root = project_root.parent

    # Define paths relative to the project root
    files_to_include = [
        # HTML Templates
        project_root / "frontend" / "templates" / "audit_trail.html",

        # JavaScript Files
        project_root / "frontend" / "static" / "js" / "audit_trail.js",
        project_root / "frontend" / "static" / "js" / "audit_trail_expand.js",
        project_root / "frontend" / "static" / "js" / "components" / "attachment_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "order_note_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "pdf_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "receive_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "shared_filters.js",
        project_root / "frontend" / "static" / "js" / "components" / "utils.js",
        project_root / "frontend" / "static" / "js" / "components" / "expand_line_items.js", # Used by other screens, but relevant for context

        # CSS Files
        project_root / "frontend" / "static" / "css" / "style.css",

        # Backend Python Files
        project_root / "backend" / "main.py",
        project_root / "backend" / "database.py",
        project_root / "backend" / "utils" / "permissions_utils.py",
        project_root / "backend" / "endpoints" / "audit_trail_filters.py",
        project_root / "backend" / "endpoints" / "orders.py",
        project_root / "backend" / "endpoints" / "order_queries.py",
        project_root / "backend" / "endpoints" / "order_receiving.py",
        project_root / "backend" / "endpoints" / "lookups" / "users.py", # For users table schema/management
    ]

    # Database Path
    db_path = project_root / "data" / "orders.db"

    # Determine desktop path (cross-platform basic attempt)
    desktop_path = Path.home() / "Desktop"
    output_filename = "audit_trail_files.txt"
    output_file_path = desktop_path / output_filename

    print(f"Collecting files for Audit Trail screen and database schema...")

    with open(output_file_path, "w", encoding="utf-8") as outfile:
        outfile.write(f"--- Audit Trail Screen Files and Database Schema Dump ---\n\n")
        outfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write(f"Project Root: {project_root}\n\n")

        # Include Database Schema
        outfile.write("=" * 80 + "\n")
        outfile.write("DATABASE SCHEMA:\n")
        outfile.write("=" * 80 + "\n")
        if db_path.exists():
            schema_content = get_db_schema(db_path)
            outfile.write(schema_content + "\n")
        else:
            outfile.write(f"WARNING: Database file not found at {db_path}\n\n")

        # Include contents of each specified file
        for file_path in files_to_include:
            outfile.write("=" * 80 + "\n")
            outfile.write(f"FILE: {file_path.relative_to(project_root)}\n")
            outfile.write("=" * 80 + "\n")
            if file_path.exists():
                content = get_file_content(file_path)
                outfile.write(content + "\n")
            else:
                outfile.write(f"WARNING: File not found at {file_path.relative_to(project_root)}\n")
            outfile.write("\nEND OF FILE\n\n")

    print(f"Successfully generated dump file at: {output_file_path}")

if __name__ == "__main__":
    main()