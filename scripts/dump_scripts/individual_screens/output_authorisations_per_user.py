# File: generate_authorisations_files_dump.py
# This script collects all files related to order authorisations,
# including settings, desktop and mobile authorisation screens,
# and relevant database schemas, outputting them to a single text file on the user's desktop.

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
        # Fetch schema for tables relevant to authorisations
        relevant_tables = [
            "orders", "order_items", "settings", "users",
            "audit_trail", "screen_permissions"
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

    # Define paths relative to the project root for authorisation functionality
    files_to_include = [
        # Frontend HTML Templates (Authorisation Screens)
        project_root / "frontend" / "templates" / "authorisations_per_user.html", # Desktop "My Authorisations"
        project_root / "frontend" / "templates" / "mobile" / "mobile_authorisations.html", # Mobile Authorisations
        project_root / "frontend" / "templates" / "mobile" / "mobile_login.html", # Mobile login leading to auth
        project_root / "frontend" / "templates" / "login.html", # Desktop login leading to auth
        project_root / "frontend" / "templates" / "_tab_nav.html", # Navigation bar showing auth links
        project_root / "frontend" / "templates" / "base.html", # Base template structure
        project_root / "frontend" / "templates" / "access_denied.html", # For permission denied scenarios

        # Frontend JavaScript Files (Authorisation Logic & Dependencies)
        project_root / "frontend" / "static" / "js" / "authorisations_per_user.js", # Main logic for desktop auth
        project_root / "frontend" / "static" / "js" / "mobile" / "js" / "authorisations_screen" / "mobile_main.js", # Main logic for mobile auth
        project_root / "frontend" / "static" / "js" / "login.js", # Redirect logic after login based on permissions
        project_root / "frontend" / "static" / "js" / "pending_orders.js", # Orders become "Awaiting Authorisation" here
        project_root / "frontend" / "static" / "js" / "new_order_main.js", # Logic for setting order status to "Awaiting Authorisation"
        project_root / "frontend" / "static" / "js" / "new_order_screen" / "submit_utils.js", # Determines auth band
        project_root / "frontend" / "static" / "js" / "audit_trail.js", # Displays authorisation status and user
        project_root / "frontend" / "static" / "js" / "audit_trail_test.js", # Displays authorisation status and user
        project_root / "frontend" / "static" / "js" / "components" / "shared_filters.js", # Filters for auth screens
        project_root / "frontend" / "static" / "js" / "components" / "expand_line_items.js", # Used to expand order details on auth screens
        project_root / "frontend" / "static" / "js" / "components" / "pdf_modal.js", # For viewing PDFs from auth screen
        project_root / "frontend" / "static" / "js" / "components" / "mobile_pdf_modal.js", # For viewing PDFs from mobile auth screen
        project_root / "frontend" / "static" / "js" / "maintenance_screen" / "users.js", # For setting user auth bands and screen permissions
        project_root / "frontend" / "static" / "js" / "maintenance_screen" / "settings.js", # For setting global auth thresholds
        project_root / "frontend" / "static" / "js" / "components" / "utils.js", # General utilities used across frontend

        # Frontend CSS
        project_root / "frontend" / "static" / "css" / "style.css", # General styling
        project_root / "frontend" / "static" / "mobile" / "css" / "mobile_authorisations.css", # Mobile specific styling

        # Backend Python Endpoints (Core Authorisation Logic)
        project_root / "backend" / "endpoints" / "orders.py", # Order creation, status updates related to auth
        project_root / "backend" / "endpoints" / "order_queries.py", # Fetching pending/awaiting authorisation orders
        project_root / "backend" / "endpoints" / "mobile" / "mobile_awaiting_authorisation.py", # Mobile API for fetching/authorising orders
        project_root / "backend" / "endpoints" / "mobile" / "mobile_auth.py", # Mobile login/session management
        project_root / "backend" / "endpoints" / "auth.py", # User authentication, session creation, screen permissions lookup
        project_root / "backend" / "endpoints" / "lookups" / "settings.py", # Managing authorisation thresholds
        project_root / "backend" / "endpoints" / "lookups" / "users.py", # User management (assigning auth bands, screen permissions)
        project_root / "backend" / "endpoints" / "audit_trail_filters.py", # Filtering and displaying audit trail for auth actions
        project_root / "backend" / "main.py", # FastAPI app setup and router inclusion
        project_root / "backend" / "database.py", # Database interactions: `determine_status_and_band`, `create_order` and updates related to status/auth band, `users` table
        project_root / "backend" / "utils" / "permissions_utils.py", # `require_login`, `require_screen_permission`, `enforce_roles`
        project_root / "backend" / "utils" / "db_utils.py", # Database utilities and error handling
        project_root / "backend" / "utils" / "order_utils.py", # `calculate_order_total` (used for determining auth band)
        project_root / "backend" / "twilio" / "twilio_utils.py", # If Twilio is used for auth notifications
        project_root / "backend" / "endpoints" / "whatsapp.py", # If WhatsApp is used for auth notifications
    ]

    # Database Path
    db_path = project_root / "data" / "orders.db"

    # Determine desktop path (cross-platform basic attempt)
    desktop_path = Path.home() / "Desktop"
    output_filename = "authorisations_functionality_dump.txt"
    output_file_path = desktop_path / output_filename

    print(f"Collecting files for 'Authorisations' functionality and relevant database schema...")

    with open(output_file_path, "w", encoding="utf-8") as outfile:
        outfile.write(f"--- Authorisations Functionality Files and Database Schema Dump ---\n\n")
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