import subprocess
import sys
from pathlib import Path
from datetime import datetime
import os
import shutil
import time

# --- Configuration ---
PROJECT_ROOT = Path("/home/steven_cohen714/orders_project")
BACKUP_DIR_NAME = "data_backup"

# Database configuration (for reference, not directly manipulated by Git)
DB_NAME = "orders.db"
LIVE_DB_PATH = PROJECT_ROOT / "data" / DB_NAME

# Path for your database initialization/migration script relative to PROJECT_ROOT
DB_INIT_SCRIPT_MODULE = "backend.database"
DB_INIT_FUNCTION = "init_db"

# Path to your main FastAPI application entry point (for pgrep)
MAIN_APP_SCRIPT = PROJECT_ROOT / "backend" / "main.py"

# Path to your server start script
START_SERVER_SCRIPT = PROJECT_ROOT / "scripts" / "start_server.py"

# Log directories
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
SERVER_STARTUP_LOG = LOGS_DIR / "server_startup.log"
SERVER_ERROR_LOG = LOGS_DIR / "server_error.log"

# --- Utility Functions ---
def print_status(message, level="info"):
    """Prints a status message with appropriate emoji."""
    if level == "info":
        print(f"🔄 {message}")
    elif level == "success":
        print(f"✅ {message}")
    elif level == "warning":
        print(f"⚠️ {message}")
    elif level == "error":
        print(f"❌ {message}")

def run_command(cmd, desc=None, check=True, cwd=PROJECT_ROOT):
    """
    Runs a shell command using the system Python and pip.
    """
    if desc:
        print_status(desc)

    cmd_list = [str(arg) for arg in cmd]

    process = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True, encoding='utf-8', shell=False)

    if check and process.returncode != 0:
        print_status(f"Error during: {desc or ' '.join(cmd_list)}", "error")
        print("--- STDOUT ---")
        print(process.stdout.strip())
        print("--- STDERR ---")
        print(process.stderr.strip())
        sys.exit(1)
    elif process.returncode != 0:
        print_status(f"Warning during: {desc or ' '.join(cmd_list)}")
        print("--- STDOUT ---")
        print(process.stdout.strip())
        print("--- STDERR ---")
        print(process.stderr.strip())
    return process

def kill_server():
    """Finds and kills the running FastAPI server process."""
    print_status("Checking for running server process...")
    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        shell=False
    )
    pids_to_kill = []
    for line in result.stdout.splitlines():
        if str(MAIN_APP_SCRIPT) in line or str(START_SERVER_SCRIPT) in line:
            parts = line.split()
            if len(parts) > 1 and parts[1].isdigit():
                pids_to_kill.append(parts[1])

    if pids_to_kill:
        for pid in set(pids_to_kill):
            print_status(f"Killing server process with PID {pid}", "info")
            try:
                subprocess.run(["kill", pid], check=True, shell=False)
                time.sleep(2)
                subprocess.run(["kill", "-0", pid], check=True, shell=False)
                print_status(f"Server process PID {pid} still alive, forcing kill.", "warning")
                subprocess.run(["kill", "-9", pid], check=True, shell=False)
            except subprocess.CalledProcessError:
                print_status(f"Server process PID {pid} successfully terminated.", "success")
            except Exception as e:
                print_status(f"Error killing PID {pid}: {e}", "error")
        print_status("Server shutdown sequence initiated.", "success")
    else:
        print_status("No server process found.", "success")

def apply_db_migrations():
    """
    Runs the init_db function from backend/database.py to apply any new schema changes.
    This function should be designed to ONLY apply schema updates and NOT delete data.
    """
    print_status("Applying database migrations (running init_db)...")
    init_db_command = [
        "python3",
        "-c",
        f"from {DB_INIT_SCRIPT_MODULE} import {DB_INIT_FUNCTION}; {DB_INIT_FUNCTION}()"
    ]
    run_command(init_db_command, desc="Executing init_db script", cwd=PROJECT_ROOT)
    print_status("Database migrations applied.", "success")

# --- Main Deployment Steps ---
def main():
    print("\n🚀 Starting deployment to Google VM (Data-Safe)...")
    
    # Check for the existence of the live data directory
    live_data_path = PROJECT_ROOT / "data"
    backup_path = None
    
    if live_data_path.exists():
        print_status(f"Live data directory found at '{live_data_path}'. Creating a fresh backup...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = live_data_path.parent / f"{BACKUP_DIR_NAME}_{timestamp}"
        try:
            # --- MODIFICATION ---
            # Copy the entire data directory, including subfolders and files.
            shutil.copytree(live_data_path, backup_path)
            print_status(f"✅ Initial live data directory backed up to '{backup_path}'.", "success")
        except Exception as e:
            print_status(f"❌ Failed to create initial backup of data directory. Aborting pull to prevent data loss: {e}", "error")
            sys.exit(1)

    # 2. Kill any running server instances
    kill_server()

    # 3. Perform Git sync (fetch, hard reset)
    print_status("Performing Git synchronization...")
    # The '.gitignore' file should contain 'data/' to prevent this folder from being tracked.
    # We explicitly remove the DB file from the git index to be extra safe.
    run_command(["git", "rm", "--cached", str(live_data_path)], "Untracking DB file from Git index", check=False, cwd=PROJECT_ROOT)
    run_command(["git", "fetch", "origin"], "Fetching latest from origin", cwd=PROJECT_ROOT)
    run_command(["git", "reset", "--hard", "origin/main"], "Hard reset to remote main", cwd=PROJECT_ROOT)
    print_status("Git sync complete. VM now matches GitHub.", "success")

    # 4. Restore the live data directory from the backup.
    if backup_path and live_data_path.exists():
        print_status(f"Restoring live data directory from backup '{backup_path}'...")
        try:
            # --- MODIFICATION ---
            # First, remove the existing data directory before restoring.
            shutil.rmtree(live_data_path)
            # Then, restore the full backup.
            shutil.copytree(backup_path, live_data_path)
            print_status("✅ Live data directory restored.", "success")
        except Exception as e:
            print_status(f"❌ Failed to restore data directory from backup: {e}. Live data state is now unpredictable. You will need to manually restore from a separate backup.", "error")
            sys.exit(1)

    # 5. Install Python dependencies (system-wide)
    print_status("Installing/Updating Python dependencies...", "info")
    run_command(["pip3", "install", "-r", "requirements.txt"], "Updating packages", cwd=PROJECT_ROOT)
    print_status("Python dependencies updated.", "success")

    # 6. Apply database migrations to the existing database
    apply_db_migrations()

    # 7. Start the server in the background using system Python
    print_status("Starting the FastAPI server...", "info")
    start_cmd_list = [
        "nohup",
        "python3",
        str(START_SERVER_SCRIPT)
    ]
    subprocess.Popen(start_cmd_list, cwd=PROJECT_ROOT,
                     stdout=open(SERVER_STARTUP_LOG, "a"),
                     stderr=open(SERVER_ERROR_LOG, "a"),
                     preexec_fn=os.setpgrp)
    print_status(f"Server started in the background. Check {SERVER_STARTUP_LOG.name} for output.", "success")
    print("\n✨ Deployment complete. Verify application functionality.")

if __name__ == "__main__":
    main()