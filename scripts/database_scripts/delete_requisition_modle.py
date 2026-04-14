# File: delete_requisition_module.py
# This script automates the deletion of requisition-related files and DB tables.
# It DOES NOT modify backend/main.py or frontend/templates/_tab_nav.html.
# These must be updated manually after running this script.

import subprocess
import os
import sys
from pathlib import Path
import sqlite3
import time

# --- Configuration ---
PROJECT_ROOT = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
DB_PATH = PROJECT_ROOT / "data" / "orders.db"

# --- Helper Function to Run Shell Commands ---
def run_command(cmd, desc="", check=True, shell=False, cwd=PROJECT_ROOT):
    print(f"🔄 {desc}...")
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, check=check, text=True, capture_output=True, cwd=cwd)
        else:
            result = subprocess.run(cmd, check=check, text=True, capture_output=True, cwd=cwd)
        print(f"✅ {desc} complete.")
        if result.stdout:
            print(f"--- STDOUT ---\n{result.stdout.strip()}")
        if result.stderr and not check: # Only print stderr if not strictly checking and there's output
            print(f"--- STDERR ---\n{result.stderr.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during: {desc}")
        print("--- STDOUT ---")
        print(e.stdout.strip())
        print("--- STDERR ---")
        print(e.stderr.strip())
        sys.exit(1) # Exit if a critical command fails
    except Exception as e:
        print(f"❌ Unexpected error during: {desc} - {e}")
        sys.exit(1)

# --- Main Deletion Logic ---
def main():
    print("🚀 Starting complete deletion of Requisition Module components...")

    # 1. Stop FastAPI Server
    run_command([str(PROJECT_ROOT / "scripts" / "stop_server.py")], "Stopping FastAPI server")
    # Aggressive kill for any lingering processes
    run_command(
        f"ps aux | grep python | grep {PROJECT_ROOT.name} | awk '{{print $2}}' | xargs kill -9",
        "Aggressively killing lingering Python processes",
        check=False, # Don't exit if no processes found
        shell=True
    )
    time.sleep(1) # Give processes a moment to die

    # 2. Database Cleanup
    print("\n--- Cleaning up Database Tables ---")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        tables_to_drop = ["requisition_attachments", "requisition_items", "requisitions", "requisitioners"]
        for table in tables_to_drop:
            run_command(f"DROP TABLE IF EXISTS {table};", f"Dropping table {table}", shell=True, cwd=None, check=False) # Run directly in SQLite
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table};")
                conn.commit()
                print(f"✅ Table {table} dropped in DB.")
            except sqlite3.Error as e:
                print(f"⚠️ Could not drop table {table} in DB: {e}. It might not exist or be locked.")
        conn.close()
    except Exception as e:
        print(f"❌ Error connecting to database for cleanup: {e}")
        sys.exit(1)

    # 3. Remove Backend Python Files
    print("\n--- Removing Backend Python Files ---")
    backend_endpoints_dir = PROJECT_ROOT / "backend" / "endpoints"
    backend_lookups_dir = backend_endpoints_dir / "lookups"
    backend_mobile_dir = backend_endpoints_dir / "mobile"

    files_to_delete = [
        backend_endpoints_dir / "requisitions.py",
        backend_endpoints_dir / "requisition_attachments.py",
        backend_lookups_dir / "requisitioners.py",
        backend_mobile_dir / "mobile_requisition_auth.py",
        backend_mobile_dir / "mobile_requisition.py",
    ]
    for file_path in files_to_delete:
        if file_path.exists():
            run_command(f"rm {file_path}", f"Deleting {file_path.name}")
        else:
            print(f"ℹ️ {file_path.name} not found, skipping.")

    # 4. Clear Python Bytecode Caches for these directories
    print("\n--- Clearing Python Bytecode Caches ---")
    for cache_dir in [
        backend_endpoints_dir / "__pycache__",
        backend_lookups_dir / "__pycache__",
        backend_mobile_dir / "__pycache__",
    ]:
        if cache_dir.exists():
            run_command(f"rm -rf {cache_dir}", f"Deleting {cache_dir.name} in {cache_dir.parent.name}")
        else:
            print(f"ℹ️ {cache_dir.name} not found, skipping.")

    # 5. Remove Frontend JavaScript Files
    print("\n--- Removing Frontend JavaScript Files ---")
    frontend_js_dir = PROJECT_ROOT / "frontend" / "static" / "js"
    frontend_maintenance_dir = frontend_js_dir / "maintenance_screen"
    frontend_components_dir = frontend_js_dir / "components"

    js_files_to_delete = [
        frontend_js_dir / "new_requisition_main.js",
        frontend_js_dir / "pending_requisitions.js",
        frontend_js_dir / "new_requisitions_pdf_generator.py", # Python file in JS dir
        frontend_maintenance_dir / "requisitioners.js",
        frontend_components_dir / "expand_requisition_items.js",
        frontend_components_dir / "requisitions_attachment_modal.js",
    ]
    for file_path in js_files_to_delete:
        if file_path.exists():
            run_command(f"rm {file_path}", f"Deleting {file_path.name}")
        else:
            print(f"ℹ️ {file_path.name} not found, skipping.")

    # 6. Remove HTML Template Files
    print("\n--- Removing HTML Template Files ---")
    templates_dir = PROJECT_ROOT / "frontend" / "templates"
    html_files_to_delete = [
        templates_dir / "new_requisition.html",
        templates_dir / "pending_requisitions.html",
    ]
    for file_path in html_files_to_delete:
        if file_path.exists():
            run_command(f"rm {file_path}", f"Deleting {file_path.name}")
        else:
            print(f"ℹ️ {file_path.name} not found, skipping.")

    print("\n--- Automated Deletion Complete ---")
    print("\n")
    print("####################################################################")
    print("###               MANUAL STEPS REQUIRED NEXT                     ###")
    print("####################################################################")
    print("\n")
    print("1.  UPDATE backend/main.py:")
    print("    Open /Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py")
    print("    DELETE ALL lines that import or include ANY requisition-related routers.")
    print("    Look for and remove lines like:")
    print("        from backend.endpoints import requisitions")
    print("        from backend.endpoints import requisition_attachments")
    print("        from backend.endpoints.mobile import mobile_requisition_auth")
    print("        from backend.endpoints.mobile import mobile_requisition")
    print("        from backend.endpoints.lookups import requisitioners as requisitioners_router")
    print("")
    print("        app.include_router(requisitions.router)")
    print("        app.include_router(requisitioners_router.router, prefix=\"/lookups\")")
    print("        app.include_router(requisition_attachments.router, prefix=\"/requisitions\")")
    print("        app.include_router(mobile_requisition_auth.router)")
    print("        app.include_router(mobile_requisition.router)")
    print("    (Be careful within the 'for router_item in routers:' loop if it includes any.)")
    print("    SAVE backend/main.py.")
    print("\n")
    print("2.  UPDATE frontend/templates/_tab_nav.html:")
    print("    Open /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/templates/_tab_nav.html")
    print("    DELETE the HTML blocks for 'New Requisition' and 'Pending Requisitions' buttons:")
    print("        {% if \"new_requisition\" in user_screen_permissions %}")
    print("        <button onclick=\"location.href='/requisitions/new'\">New Requisition</button>")
    print("        {% endif %}")
    print("        {% if \"pending_requisitions\" in user_screen_permissions %}")
    print("        <button onclick=\"location.href='/requisitions/pending_requisitions'\">Pending Requisitions</button>")
    print("        {% endif %}")
    print("    SAVE _tab_nav.html.")
    print("\n")
    print("3.  RESTART your FastAPI server MANUALLY after completing the above manual steps:")
    print("    cd /Users/stevencohen/Projects/universal_recycling/orders_project")
    print("    python -m uvicorn backend.main:app --host 0.0.0.0 --port 8004 --reload --log-level debug")
    print("    Perform a HARD REFRESH in your browser.")
    print("\n")
    print("You should now have no requisition-related errors and a clean slate.")

if __name__ == "__main__":
    main()