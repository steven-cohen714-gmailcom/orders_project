#orders_project/scripts/Local_machine_git_scripts/pull_and_start.py

import subprocess
import os
import sys
from pathlib import Path
import shutil

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
UVICORN_APP = "backend.main:app"
HOST = "0.0.0.0"
PORT = 8004

def run_command(cmd, desc=None, check=True):
    """
    Runs a shell command and checks for errors.
    """
    if desc:
        print(f"🔧 {desc}")
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, check=check)
    return result

def create_gitignore_file():
    """
    Ensures a .gitignore exists and contains necessary entries.
    """
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("venv/\n")
            f.write("logs/\n")
            f.write("data/\n")
            f.write(".DS_Store\n")
            f.write("__pycache__/\n")
        print("✅ .gitignore file created.")
    
def main():
    print(f"🚀 Starting fresh deployment on local machine...")
    
    # 1. Ensure .gitignore is set up correctly
    create_gitignore_file()

    # 2. Kill any running server instances (if any)
    # This is handled by a different script.
    
    # 3. Clean and pull latest from GitHub
    print("🔄 Pulling latest changes from GitHub...")
    run_command(["git", "fetch", "origin"], "Fetching changes")
    run_command(["git", "reset", "--hard", "origin/main"], "Overwriting local files to match GitHub")

    # 4. Re-create virtual environment and install dependencies
    print("🔄 Re-creating virtual environment and installing dependencies...")
    venv_dir = PROJECT_ROOT / "venv"
    if venv_dir.exists():
        run_command(["rm", "-rf", str(venv_dir)], "Deleting old virtual environment")
    
    run_command([sys.executable, "-m", "venv", "venv"], "Creating new virtual environment")
    run_command(["./venv/bin/pip", "install", "-r", "requirements.txt"], "Installing dependencies")
    print("✅ Environment setup complete.")

    # 5. Start the server
    print(f"🚀 Launching Uvicorn: {UVICORN_APP} on port {PORT}...")
    run_command([
        "./venv/bin/uvicorn",
        UVICORN_APP,
        "--host", HOST,
        "--port", str(PORT),
        "--reload"
    ], "Starting server in the foreground")

if __name__ == "__main__":
    main()