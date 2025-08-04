# File: generate_new_order_files_dump.py
# This script collects all files related to creating and managing new orders
# and the relevant database schemas, outputting them to a single text file on the user's desktop.

import os
import sys
from pathlib import Path
import sqlite3
from datetime import datetime

def get_db_schema(db_path):
    """Connects to the SQLite database and extracts its schema."""
    schema = ""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Fetch schema for tables relevant to new orders
        relevant_tables = [
            "orders", "order_items", "requesters", "suppliers",
            "projects", "items", "business_details", "settings", "users",
            "attachments", "audit_trail", "requisitions", "requisition_items" # Requisitions can be converted to orders
        ]
        for table_name in relevant_tables:
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            table_schema = cursor.fetchone()
            if table_schema:
                schema += f"{table_schema[0]};\n\n"
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
    script_path = Path(__file__).resolve()
    project_root = script_path
    # Traverse up until 'backend' and 'frontend' directories are found
    while not (project_root / "backend").is_dir() or not (project_root / "frontend").is_dir():
        if project_root.parent == project_root:
            print("Error: Could not determine project root. Please run this script from within your project directory.")
            sys.exit(1)
        project_root = project_root.parent

    # Define paths relative to the project root for new order functionality
    files_to_include = [
        # Frontend HTML Templates
        project_root / "frontend" / "templates" / "new_order.html",
        project_root / "frontend" / "templates" / "_tab_nav.html", # For navigation context
        project_root / "frontend" / "templates" / "base.html", # Base template structure
        project_root / "frontend" / "templates" / "pdf_template.html", # Used for new order PDF preview

        # Frontend JavaScript Files
        project_root / "frontend" / "static" / "js" / "new_order_main.js",
        project_root / "frontend" / "static" / "js" / "new_order_screen" / "pdf_utils.js",
        project_root / "frontend" / "static" / "js" / "new_order_screen" / "submit_utils.js",
        project_root / "frontend" / "static" / "js" / "components" / "fuzzy_dropdown.js",
        project_root / "frontend" / "static" / "js" / "components" / "utils.js", # For logToServer and populateDropdown
        project_root / "frontend" / "static" / "js" / "components" / "order_note_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "attachment_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "pdf_modal.js",
        project_root / "frontend" / "static" / "js" / "login.js", # Login success redirects to new_order sometimes

        # Frontend CSS
        project_root / "frontend" / "static" / "css" / "style.css",
        project_root / "frontend" / "static" / "css" / "fuzzy_dropdown_fix.css",

        # Backend Python Endpoints
        project_root / "backend" / "endpoints" / "orders.py", # Main order creation/update logic
        project_root / "backend" / "endpoints" / "new_order_pdf_generator.py",
        project_root / "backend" / "endpoints" / "order_attachments.py", # For attachments on new orders
        project_root / "backend" / "endpoints" / "order_notes.py", # For notes on new orders
        project_root / "backend" / "endpoints" / "html_routes.py", # Route for rendering new_order.html
        project_root / "backend" / "endpoints" / "utils.py", # For client-side logging
        project_root / "backend" / "endpoints" / "auth.py", # For user session and login which impacts access
        project_root / "backend" / "endpoints" / "email_service.py", # For emailing the new order PDF

        # Backend Lookup Endpoints (data source for new order form dropdowns)
        project_root / "backend" / "endpoints" / "lookups" / "requesters.py",
        project_root / "backend" / "endpoints" / "lookups" / "suppliers.py",
        project_root / "backend" / "endpoints" / "lookups" / "items.py",
        project_root / "backend" / "endpoints" / "lookups" / "projects.py",
        project_root / "backend" / "endpoints" / "lookups" / "settings.py", # For order number and auth thresholds
        project_root / "backend" / "endpoints" / "lookups" / "business_details.py", # For company address
        project_root / "backend" / "endpoints" / "lookups" / "users.py", # User permissions relevant to who can create orders

        # Core Backend Files
        project_root / "backend" / "main.py", # FastAPI app, router inclusion
        project_root / "backend" / "database.py", # Database connection, schema init, core CRUD operations like create_order
        project_root / "backend" / "utils" / "permissions_utils.py", # Login and screen permission enforcement
        project_root / "backend" / "utils" / "db_utils.py", # Database error handling and logging
        project_root / "backend" / "utils" / "order_utils.py", # Calculate order total, normalize order number
        project_root / "backend" / "utils" / "send_email.py", # Email sending utility
    ]

    # Database Path
    db_path = project_root / "data" / "orders.db"

    # Determine desktop path (cross-platform basic attempt)
    desktop_path = Path.home() / "Desktop"
    output_filename = "new_order_functionality_dump.txt"
    output_file_path = desktop_path / output_filename

    print(f"Collecting files for 'New Order' functionality and relevant database schema...")

    with open(output_file_path, "w", encoding="utf-8") as outfile:
        outfile.write(f"--- New Order Functionality Files and Database Schema Dump ---\n\n")
        outfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write(f"Project Root: {project_root}\n\n")

        # Include Database Schema
        outfile.write("=" * 80 + "\n")
        outfile.write("DATABASE SCHEMA (Relevant Tables):\n")
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