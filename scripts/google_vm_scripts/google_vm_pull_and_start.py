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
# VENV_ACTIVATE_SCRIPT is not strictly needed with the direct executable approach
# VENV_ACTIVATE_SCRIPT = VENV_PATH / "bin" / "activate"

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
    Runs a shell command. If in_venv is True, uses the virtual environment's
    executables directly instead of sourcing the activate script.
    """
    if desc:
        print_status(desc)

    cmd_list = [str(arg) for arg in cmd]

    if in_venv:
        # Determine the correct Python/pip path within the venv
        venv_python = VENV_PATH / "bin" / "python3" # Explicitly use python3 within venv
        venv_pip = VENV_PATH / "bin" / "pip"

        if not venv_python.exists():
            print_status(f"Virtual environment Python executable not found at {venv_python}", "error")
            sys.exit(1)
            
        # Adjust the command to use the venv's executables
        if cmd_list[0] == "python" or cmd_list[0] == "python3":
            cmd_list[0] = str(venv_python)
        elif cmd_list[0] == "pip": # Replace 'pip' with the full venv pip path
            cmd_list[0] = str(venv_pip)
            
        # Ensure that if the command is "python -m pip install", it uses the venv's python
        if len(cmd_list) > 1 and cmd_list[1] == "-m" and cmd_list[2] == "pip":
            cmd_list[0] = str(venv_python) # Ensure the first part is the venv python
            # cmd_list remains the same for -m pip install ...
        
        process = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True, encoding='utf-8', shell=False) # Explicitly set shell=False
    else:
        # Run directly without venv-specific adjustments
        process = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True, encoding='utf-8', shell=False) # Explicitly set shell=False

    if check and process.returncode != 0:
        print_status(f"Error during: {desc or ' '.join(cmd_list)}", "error")
        print("--- STDOUT ---")
        print(process.stdout.strip())
        print("--- STDERR ---")
        print(process.stderr.strip())
        sys.exit(1)
    elif process.returncode != 0: # This block handles non-zero exit codes that are not critical errors
        print_status(f"Warning during: {desc or ' '.join(cmd_list)}")
        print("--- STDOUT ---")
        print(process.stdout.strip())
        print("--- STDERR ---")
        print(process.stderr.strip())
    return process

def kill_server():
    """Finds and kills the running FastAPI server process."""
    print_status("Checking for running server process...")
    # Use the venv's python path for more accurate process identification
    venv_python_path = VENV_PATH / "bin" / "python3" # Changed to python3

    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        shell=False # Ensure no shell is used here either
    )
    pids_to_kill = []
    for line in result.stdout.splitlines():
        # Check for processes running with the venv's python or uvicorn
        if (str(venv_python_path) in line and (str(MAIN_APP_SCRIPT) in line or str(START_SERVER_SCRIPT) in line)) or \
           ("uvicorn" in line and str(venv_python_path) in line): # Ensure uvicorn is from THIS venv
            parts = line.split()
            if len(parts) > 1 and parts[1].isdigit():
                pids_to_kill.append(parts[1])

    if pids_to_kill:
        # Use set to avoid attempting to kill the same PID multiple times
        for pid in set(pids_to_kill):
            print_status(f"Killing server process with PID {pid}", "info")
            try:
                # Attempt graceful termination first
                subprocess.run(["kill", pid], check=True, shell=False) # SIGTERM
                time.sleep(2) # Give it a moment to shut down
                # Check if process is still alive (kill -0)
                subprocess.run(["kill", "-0", pid], check=True, shell=False) 
                # If it's still alive, force kill
                print_status(f"Server process PID {pid} still alive, forcing kill.", "warning")
                subprocess.run(["kill", "-9", pid], check=True, shell=False)
            except subprocess.CalledProcessError:
                # This means kill -0 failed, implying the process is gone (good!)
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
        "python3", # This will be replaced by the venv's python3 in run_command
        "-c",
        f"from {DB_INIT_SCRIPT_MODULE} import {DB_INIT_FUNCTION}; {DB_INIT_FUNCTION}()"
    ]
    run_command(init_db_command, desc="Executing init_db script", cwd=PROJECT_ROOT, in_venv=True)
    print_status("Database migrations applied.", "success")


# --- Main Deployment Steps ---
def main():
    print("\n🚀 Starting deployment to Google VM (Data-Safe)...")

    # 1. First Safety Check: Backup the live database before starting anything.
    if LIVE_DB_PATH.exists():
        print_status(f"Live database found at '{LIVE_DB_PATH}'. Creating a fresh backup...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        first_backup_path = LIVE_DB_PATH.parent / f"{LIVE_DB_PATH.name}.pre_pull_backup_{timestamp}"
        try:
            shutil.copy2(LIVE_DB_PATH, first_backup_path)
            print_status(f"✅ Initial live database backed up to '{first_backup_path}'.", "success")
        except Exception as e:
            print_status(f"❌ Failed to create initial backup. Aborting pull to prevent data loss: {e}", "error")
            sys.exit(1)
    
    # 2. Kill any running server instances
    kill_server()

    # 3. Perform Git sync (fetch, hard reset)
    # This assumes 'data/' is in .gitignore and will NOT be touched by git.
    print_status("Performing Git synchronization...")
    
    # Run 'git rm --cached' to ensure the DB file is no longer tracked by Git.
    # This prevents an outdated DB from ever being pulled and overwriting the live one.
    run_command(["git", "rm", "--cached", str(LIVE_DB_PATH)], "Untracking DB file from Git index", check=False, cwd=PROJECT_ROOT)

    run_command(["git", "fetch", "origin"], "Fetching latest from origin", cwd=PROJECT_ROOT)
    run_command(["git", "reset", "--hard", "origin/main"], "Hard reset to remote main", cwd=PROJECT_ROOT)
    # The `git clean` command is destructive and can be dangerous, so we'll omit it for maximum safety.
    # If you need it, uncomment the following line:
    # run_command(["git", "clean", "-fd"], "Removing untracked files and directories", cwd=PROJECT_ROOT)
    print_status("Git sync complete. VM now matches GitHub.", "success")

    # 4. Restore the live database from the backup.
    if LIVE_DB_PATH.exists():
        print_status(f"Restoring live database from backup '{first_backup_path}'...")
        try:
            shutil.copy2(first_backup_path, LIVE_DB_PATH)
            print_status("✅ Live database restored.", "success")
        except Exception as e:
            print_status(f"❌ Failed to restore database from backup: {e}. Live database state is now unpredictable. You will need to manually restore from a separate backup.", "error")
            sys.exit(1)

    # 5. Ensure virtual environment is set up
    print_status("Ensuring virtual environment exists and is up-to-date...")
    if not VENV_PATH.exists():
        print_status(f"Virtual environment not found at {VENV_PATH}. Creating it...", "info")
        run_command([sys.executable, "-m", "venv", str(VENV_PATH)], "Creating virtual environment", cwd=PROJECT_ROOT, check=True)
        print_status("Virtual environment created.", "success")
    else:
        print_status("Virtual environment already exists.", "info")

    # 6. Install Python dependencies (within the venv)
    print_status("Installing/Updating Python dependencies...", "info")
    run_command(["python3", "-m", "pip", "install", "-r", "requirements.txt"], "Updating virtualenv packages", cwd=PROJECT_ROOT, in_venv=True)
    print_status("Python dependencies updated.", "success")

    # 7. Apply database migrations to the existing database
    apply_db_migrations()

    # 8. Start the server in the background using nohup and the venv's python
    print_status("Starting the FastAPI server...", "info")
    start_cmd_list = [
        "nohup",
        str(VENV_PATH / "bin" / "python3"),
        str(START_SERVER_SCRIPT)
    ]
    subprocess.Popen(start_cmd_list, cwd=PROJECT_ROOT,
                         stdout=open(SERVER_STARTUP_LOG, "a"),
                         stderr=open(SERVER_ERROR_LOG, "a"),
                         preexec_fn=os.setpgrp
                        )
    print_status(f"Server started in the background. Check {SERVER_STARTUP_LOG.name} for output.", "success")
    print("\n✨ Deployment complete. Verify application functionality.")

if __name__ == "__main__":
    main()