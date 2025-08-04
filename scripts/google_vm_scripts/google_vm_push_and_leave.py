# File: orders_project/scripts/google_vm_scripts/google_vm_push_and_leave.py

import subprocess
import socket
import sys
from pathlib import Path
import os
import time

# --- Configuration for Safety Check ---
EXPECTED_HOSTNAME = "universal-recycling-google-server"

# --- Determine the project root dynamically ---
# This script is located at: orders_project/scripts/google_vm_scripts/
# We need to go up two levels to get to the 'orders_project' root.
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent

# --- Safety Check: Ensure we are on the correct server ---
current_hostname = socket.gethostname()
if current_hostname != EXPECTED_HOSTNAME:
    print(f"❌ SECURITY ABORT: This script is for the Google VM only.")
    print(f"   Expected hostname: '{EXPECTED_HOSTNAME}'")
    print(f"   Current hostname:  '{current_hostname}'")
    print("   No actions were performed.")
    sys.exit(1)
else:
    print(f"✅ Security check passed. Hostname '{current_hostname}' matches expected.")

def create_gitignore_file():
    """
    Ensures a .gitignore exists and contains necessary entries.
    """
    gitignore_path = project_root / ".gitignore"
    if not gitignore_path.exists():
        print("🔧 Creating .gitignore file...")
        with open(gitignore_path, "w") as f:
            f.write("# Ignore files that should not be in Git\n")
            f.write("venv/\n")
            f.write("logs/\n")
            f.write("data/\n")
            f.write(".DS_Store\n")
            f.write("__pycache__/\n")
        print("✅ .gitignore file created with necessary exclusions.")
    
    # We explicitly remove the `data` and `logs` directory from Git's index
    # to be certain they are never tracked.
    subprocess.run(["git", "rm", "-r", "--cached", "data"], cwd=project_root, capture_output=True, text=True)
    subprocess.run(["git", "rm", "-r", "--cached", "logs"], cwd=project_root, capture_output=True, text=True)

def run_command(cmd, desc=None, check=True):
    """
    Runs a shell command from the current working directory (project_root).
    """
    if desc:
        print(f"🔧 {desc}")
    
    result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, check=check)
    
    if result.returncode != 0:
        print(f"❌ Error during: {desc or ' '.join(cmd)}")
        print(result.stderr.strip())
        sys.exit(1)
    
    return result

def main():
    print("🧠 Staging and committing all VM project files...")

    # 1. Ensure .gitignore is set up correctly and untrack unwanted files
    create_gitignore_file()

    # 2. Stage ALL changes
    run_command(["git", "add", "-A"], "Staging ALL files")

    # 3. Commit all staged changes
    run_command(["git", "commit", "-m", f'SYNC FROM VM ({current_hostname})'], "Committing VM changes", check=False)

    # 4. Push to GitHub
    run_command(["git", "push"], "Pushing to GitHub")

    print("✅ VM state is now pushed to GitHub.")

if __name__ == "__main__":
    main()