import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime

def run_command(command, desc):
    print(f"Running: {desc}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {desc}: {e.stderr}")
        return ""

def get_database_schema(db_path):
    print(f"Fetching database schema from {db_path}")
    schema = ""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                schema += f"\n### Table `{table_name}`\n"
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    col_notnull = "not null" if col[3] else "nullable"
                    col_default = f" default {col[4]}" if col[4] is not None else ""
                    col_pk = "pk=True" if col[5] else "pk=False"
                    schema += f"- `{col_name}` ({col_type}), {col_pk}, {col_notnull}{col_default}\n"
    except sqlite3.Error as e:
        print(f"Error fetching schema: {e}")
        schema += f"Error fetching schema: {e}\n"
    return schema

def get_file_contents(file_path):
    print(f"Reading file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {file_path}\n"
    except Exception as e:
        return f"Error reading {file_path}: {e}\n"

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    output_file = repo_path / "stuff_we_are_working_on_today.md"
    db_path = repo_path / "data/orders.db"
    env_path = repo_path / ".env"

    # Introduction
    intro = f"""# 📦 Orders Project Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
The Orders Project is a custom-built Purchase Order system for Universal Recycling Company Pty Ltd, a metals recycling business in South Africa. It allows the company to create, manage, and track purchase orders through various stages: **Pending** → **Awaiting Authorisation** (for orders exceeding the threshold stored in the `settings` table under `auth_threshold`, adjustable in the Maintenance section) → **Authorised** → **Received**. The system includes features like order number generation, Twilio integration for notifications, PDF generation for purchase orders, and a maintenance section for managing company details.

- **User Base**: Less than 10 users, with only 2 having edit rights (others have view-only rights).
- **Deployment**: Hosted on a Google Cloud VM running Debian Linux.
- **Tools**: SQLite, Python, HTML, JavaScript.

## Development Environment
- **Python Version**: 3.13
- **Dependencies** (from `requirements.txt`):
  - fastapi
  - uvicorn
  - jinja2
  - python-multipart
  - twilio
  - python-dotenv

## Current Focus
Today’s tasks include:
- Fixing Twilio/ngrok integration for WhatsApp notifications (triggered when orders exceed the `auth_threshold` value in the `settings` table).
- Resolving order number increment issues (skipping numbers). Note: This may impact PDF generation, as the order number is part of the PDF.
- Updating the New Order screen to display the current order number.
- Implementing PDF generation for the "View Purchase Order" button, with email functionality (depends on fixing order number increment).
- Updating the Maintenance section to include Universal Recycling’s company details.
"""

    # Directory Structure
    dir_structure = "## 📁 Directory Structure\n```\n"
    dir_structure += run_command(["tree", "-L", "4"], "Fetching directory structure")
    dir_structure += "```\n"

    # Database Schema
    db_schema = "## 🗄️ Database Schema (`data/orders.db`)\n"
    db_schema += get_database_schema(db_path)

    # Environment Variables
    env_section = "## 🌍 Environment Variables (`.env`)\n"
    env_section += "Note: Sensitive values like Twilio SSID, auth token, and ngrok token should be stored here.\n"
    env_section += "```plaintext\n"
    env_section += get_file_contents(env_path)
    env_section += "```\n"

    # General Requirements
    general_requirements = """## 📋 General Requirements

- **Date Format**: All dates must default to today’s date, use the `dd/mm/yyyy` format (allowing `d/m/yyyy` input), and include a calendar component for selection. If possible, support navigation between date sections (day/month/year) using right/left arrow keys.
"""

    # General Notes
    general_notes = """## 📝 General Notes

- **Server URL**: The application runs on `http://localhost:8004` by default (verified in `main.py`).
- **ngrok Setup**: ngrok should be running to expose the local server for Twilio webhooks. Use the provided ngrok token and username to set up. Current ngrok URL: [To be updated after setup].
- **Twilio Webhook**: Ensure the Twilio webhook for WhatsApp is configured to point to the ngrok URL at `/orders/whatsapp/webhook`.
"""

    # Relevant Files for Current Tasks
    files_section = "## 📂 Relevant Files for Current Tasks\n"

    # Main application setup
    files_section += """### Main Application Setup (`backend/main.py`)

```python
"""
    files_section += get_file_contents(repo_path / "backend/main.py")
    files_section += "\n```\n"

    # Twilio and ngrok integration
    files_section += """### Twilio Integration (`backend/twilio/twilio_utils.py`)

**Twilio Configuration**:
- **Universal Recycling WhatsApp Number**: +27 64 847-5358 (South Africa)
- **Twilio Number**: +1 947 222 4054
- **Twilio SSID**: AC78528274fa496d197171ff628cadc23a (Note: Store securely in `.env`)
- **Twilio Auth Token**: a30638234faac92dd326e749c67d5070 (Note: Store securely in `.env`)

**ngrok Configuration**:
- **ngrok Username**: tintin@urc.co.za
- **ngrok Token**: 2wFRynZ4XvFxSsrrAMWDWeUQbd2_5NuF5uaXUD5DyLgVjW32M (Note: Store securely in `.env`)

```python
"""
    files_section += get_file_contents(repo_path / "backend/twilio/twilio_utils.py")
    files_section += "\n```\n"

    # Order number increment issue
    files_section += """### Order Number Generation (`backend/endpoints/orders.py`)

```python
"""
    files_section += get_file_contents(repo_path / "backend/endpoints/orders.py")
    files_section += "\n```\n"

    # New order screen fix
    files_section += """### New Order Screen (`frontend/templates/new_order.html`)

```html
"""
    files_section += get_file_contents(repo_path / "frontend/templates/new_order.html")
    files_section += "\n```\n"

    # PDF generation for View Purchase Order
    files_section += """### Note: PDF Generation Logic

The `View Purchase Order` button logic is in `frontend/templates/new_order.html` (above) and the `/orders` endpoint in `backend/endpoints/orders.py` (above).
"""

    # Maintenance section update
    files_section += """### Maintenance Section (`frontend/templates/maintenance.html`)

**Company Details Format**:
```
Delivery Address
Universal Recycling Company Pty Ltd
[Address Line 1 from DB]
[Address Line 2 from DB]
[City, Province, Area Code from DB]
Telephone: [Telephone from DB]
VAT Number: [VAT Number from DB]
```

```html
"""
    files_section += get_file_contents(repo_path / "frontend/templates/maintenance.html")
    files_section += "\n```\n"

    # Combine all sections
    full_content = f"{intro}\n{dir_structure}\n{db_schema}\n{env_section}\n{general_requirements}\n{general_notes}\n{files_section}"

    # Write to stuff_we_are_working_on_today.md
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ Generated {output_file}")

if __name__ == "__main__":
    main()