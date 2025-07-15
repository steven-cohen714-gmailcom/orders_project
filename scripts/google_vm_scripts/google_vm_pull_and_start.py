# deploy_to_vm.py
# This script is designed to be run directly on the Google VM.
# It will pull the latest code from GitHub, ensure the database (and data dir) are untouched,
# apply any new database schema migrations, and restart the FastAPI server.

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import os
import shutil
import time

# --- Configuration ---
PROJECT_ROOT = Path("/home/steven_cohen714/orders_project")

# Database configuration (for reference, not directly manipulated by Git)
DB_NAME = "orders.db"
LIVE_DB_PATH = PROJECT_ROOT / "data" / DB_NAME # This path should be in .gitignore

# Path for your database initialization/migration script relative to PROJECT_ROOT
DB_INIT_SCRIPT_MODULE = "backend.database" # Module path for import
DB_INIT_FUNCTION = "init_db" # Function name to call

# Path to your main FastAPI application entry point (for pgrep)
MAIN_APP_SCRIPT = PROJECT_ROOT / "backend" / "main.py"

# Path to your server start script
START_SERVER_SCRIPT = PROJECT_ROOT / "scripts" / "start_server.py"

# Virtual environment path
VENV_PATH = PROJECT_ROOT / "venv"
VENV_ACTIVATE_SCRIPT = VENV_PATH / "bin" / "activate"

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

def run_command(cmd, desc=None, check=True, cwd=PROJECT_ROOT, in_venv=False):
    """
    Runs a shell command. If in_venv is True, activates the venv before running.
    """
    if desc:
        print_status(desc)

    cmd_list = [str(arg) for arg in cmd]

    if in_venv:
        if not VENV_ACTIVATE_SCRIPT.exists():
            print_status(f"Virtual environment activation script not found at {VENV_ACTIVATE_SCRIPT}", "error")
            sys.exit(1)
        # Construct command to run within an activated sub-shell
        full_cmd_str = f"source {VENV_ACTIVATE_SCRIPT} && {' '.join(cmd_list)}"
        process = subprocess.run(full_cmd_str, cwd=cwd, capture_output=True, text=True, encoding='utf-8', shell=True)
    else:
        # Run directly without venv activation
        process = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True, encoding='utf-8')

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
    venv_python_path = VENV_PATH / "bin" / "python"
    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    pids_to_kill = []
    for line in result.stdout.splitlines():
        if str(venv_python_path) in line and (str(MAIN_APP_SCRIPT) in line or str(START_SERVER_SCRIPT) in line or "uvicorn" in line):
            parts = line.split()
            if len(parts) > 1 and parts[1].isdigit():
                pids_to_kill.append(parts[1])

    if pids_to_kill:
        for pid in set(pids_to_kill):
            print_status(f"Killing server process with PID {pid}", "info")
            try:
                subprocess.run(["kill", pid], check=True) # SIGTERM
                time.sleep(2)
                subprocess.run(["kill", "-0", pid], check=True)
                print_status(f"Server process PID {pid} still alive, forcing kill.", "warning")
                subprocess.run(["kill", "-9", pid], check=True)
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
    Ensures the active virtual environment's python is used.
    """
    print_status("Applying database migrations (running init_db)...")
    init_db_command = [
        "python3",
        "-c",
        f"from {DB_INIT_SCRIPT_MODULE} import {DB_INIT_FUNCTION}; {DB_INIT_FUNCTION}()"
    ]
    run_command(init_db_command, desc="Executing init_db script", cwd=PROJECT_ROOT, in_venv=True)
    print_status("Database migrations applied.", "success")


# --- Main Deployment Steps ---
def main():
    print("\n🚀 Starting deployment to Google VM (Data-Safe)...")

    # 1. Kill any running server instances
    kill_server()

    # 2. Perform Git sync (fetch, hard reset, clean)
    # This assumes 'data/' is in .gitignore and will NOT be touched by git.
    print_status("Performing Git synchronization...")
    run_command(["git", "fetch", "origin"], "Fetching latest from origin", cwd=PROJECT_ROOT)
    run_command(["git", "reset", "--hard", "origin/main"], "Hard reset to remote main", cwd=PROJECT_ROOT)
    # Only run git clean if you are absolutely certain no untracked, valuable files
    # exist outside of 'data/' that are NOT in .gitignore.
    # If in doubt, comment out the following line:
    # run_command(["git", "clean", "-fd"], "Removing untracked files and directories", cwd=PROJECT_ROOT)
    print_status("Git sync complete. VM now matches GitHub.", "success")

    # 3. Ensure virtual environment is set up and activate it
    print_status("Ensuring virtual environment exists and is up-to-date...")
    if not VENV_PATH.exists():
        print_status(f"Virtual environment not found at {VENV_PATH}. Creating it...", "info")
        # Use system's python3 to create venv
        run_command(["python3", "-m", "venv", str(VENV_PATH)], "Creating virtual environment", cwd=PROJECT_ROOT, check=True)
        print_status("Virtual environment created.", "success")
    else:
        print_status("Virtual environment already exists.", "info")

    # 4. Install Python dependencies (within the activated venv)
    print_status("Installing/Updating Python dependencies...", "info")
    run_command(["python3", "-m", "pip", "install", "-r", "requirements.txt"],
                "Updating virtualenv packages", cwd=PROJECT_ROOT, in_venv=True)
    print_status("Python dependencies updated.", "success")

    # 5. Apply database migrations to the existing database
    # This assumes init_db() handles schema changes gracefully without data loss.
    apply_db_migrations()

    # 6. Start the server
    print_status("Starting the FastAPI server...", "info")
    start_cmd_list = [
        "nohup",
        "python3",
        str(START_SERVER_SCRIPT)
    ]
    with open(SERVER_STARTUP_LOG, "a") as stdout_file, \
         open(SERVER_ERROR_LOG, "a") as stderr_file:
        subprocess.Popen(start_cmd_list, cwd=PROJECT_ROOT,
                         stdout=stdout_file,
                         stderr=stderr_file,
                         preexec_fn=os.setpgrp
                        )
    print_status(f"Server started in the background. Check {SERVER_STARTUP_LOG.name} for output.", "success")
    print("\n✨ Deployment complete. Verify application functionality.")

if __name__ == "__main__":
    main()