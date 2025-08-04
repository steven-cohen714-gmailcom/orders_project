# File: generate_email_pdf_dump.py
# This script collects all files related to emailing PDFs from within the PDF modal
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
    script_path = Path(__file__).resolve()
    project_root = script_path
    while not (project_root / "backend").is_dir() or not (project_root / "frontend").is_dir():
        if project_root.parent == project_root:
            print("Error: Could not determine project root. Please run this script from within your project directory.")
            sys.exit(1)
        project_root = project_root.parent

    # Define paths relative to the project root for emailing PDFs
    files_to_include = [
        # Frontend JavaScript Files related to PDF modal and emailing
        project_root / "frontend" / "static" / "js" / "components" / "pdf_modal.js",
        project_root / "frontend" / "static" / "js" / "components" / "attachment_modal.js", # Can open PDFs that can be emailed
        project_root / "frontend" / "static" / "js" / "new_order_screen" / "pdf_utils.js", # Triggers PDF generation and opens modal
        project_root / "frontend" / "static" / "js" / "received_orders.js", # Calls showPDFModal
        project_root / "frontend" / "static" / "js" / "pending_orders.js", # Calls showPDFModal
        project_root / "frontend" / "static" / "js" / "cod_orders.js", # Calls showPDFModal
        project_root / "frontend" / "static" / "js" / "authorisations_per_user.js", # Calls showPDFModal
        project_root / "frontend" / "static" / "js" / "audit_trail.js", # Calls showPDFModal
        project_root / "frontend" / "static" / "js" / "audit_trail_test.js", # Calls showPDFModal
        project_root / "frontend" / "static" / "js" / "new_order_main.js", # For order submission/preview logic that leads to PDF
        project_root / "frontend" / "static" / "js" / "components" / "mobile_pdf_modal.js", # Mobile specific PDF modal, also relevant
        project_root / "frontend" / "static" / "js" / "components" / "requisitions_attachment_modal.js", # Can open requisition PDFs that might have email option

        # Frontend HTML Templates displaying/using the PDF modal
        project_root / "frontend" / "templates" / "pdf_template.html",
        project_root / "frontend" / "templates" / "new_order.html", # Page where new order PDF is generated
        project_root / "frontend" / "templates" / "pending_orders.html", # Page linking to PDF view
        project_root / "frontend" / "templates" / "received_orders.html", # Page linking to PDF view
        project_root / "frontend" / "templates" / "cod_orders.html", # Page linking to PDF view
        project_root / "frontend" / "templates" / "authorisations_per_user.html", # Page linking to PDF view
        project_root / "frontend" / "templates" / "audit_trail.html", # Page linking to PDF view
        project_root / "frontend" / "templates" / "audit_trail_test.html", # Page linking to PDF view
        project_root / "frontend" / "templates" / "mobile" / "mobile_authorisations.html", # Mobile page linking to PDF view

        # Backend Python Files related to email service and PDF generation
        project_root / "backend" / "endpoints" / "email_service.py",
        project_root / "backend" / "utils" / "send_email.py",
        project_root / "backend" / "main.py", # For router inclusion
        project_root / "backend" / "database.py", # For DB interactions (e.g., supplier emails, audit trail)
        project_root / "backend" / "endpoints" / "new_order_pdf_generator.py",
        project_root / "backend" / "endpoints" / "pending_order_pdf_generator.py",
        project_root / "backend" / "endpoints" / "order_attachments.py", # For serving attachments as PDFs
        project_root / "backend" / "endpoints" / "requisition_attachments.py", # For serving requisition attachments as PDFs
        project_root / "backend" / "endpoints" / "lookups" / "suppliers.py", # For supplier email lookup/update
        project_root / "backend" / "endpoints" / "orders.py", # For order data fetching and audit trail
        project_root / "backend" / "endpoints" / "order_queries.py", # For order data fetching
        project_root / "backend" / "endpoints" / "order_notes.py", # For audit trail logging of notes (similar to email logging)
        project_root / "backend" / "endpoints" / "audit_trail_filters.py", # For audit trail data retrieval which includes email actions
        project_root / "backend" / "utils" / "permissions_utils.py", # For user authentication/permissions relevant to email logging
    ]

    # Database Path
    db_path = project_root / "data" / "orders.db"

    # Determine desktop path (cross-platform basic attempt)
    desktop_path = Path.home() / "Desktop"
    output_filename = "email_pdf_files.txt" # Changed output filename
    output_file_path = desktop_path / output_filename

    print(f"Collecting files for Emailing PDFs from PDF Modal and relevant database schema...")

    with open(output_file_path, "w", encoding="utf-8") as outfile:
        outfile.write(f"--- Emailing PDFs from PDF Modal Files and Database Schema Dump ---\n\n")
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