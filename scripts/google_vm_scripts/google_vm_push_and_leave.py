# File: /home/steven_cohen714/orders_project/scripts/google_vm_scripts/google_vm_push_and_leave.py

#!/usr/bin/env python3

import subprocess
import socket
import sys
from pathlib import Path
import os

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

# --- Change the current working directory to the project root ---
try:
    os.chdir(project_root)
    print(f"🔄 Changed current working directory to: {os.getcwd()}")
except FileNotFoundError:
    print(f"❌ Error: Project root directory not found at {project_root}")
    sys.exit(1)

def run_command(cmd, desc=None, check=True):
    """
    Runs a shell command from the current working directory (project_root).
    """
    if desc:
        print(f"🔧 {desc}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Error during: {desc or ' '.join(cmd)}")
        print(result.stderr.strip())
        sys.exit(1)
    
    return result

print("🧠 Staging and committing all VM project files...")
run_command(["git", "add", "-A"], "Staging ALL files")

run_command(["git", "commit", "-m", f'SYNC FROM VM ({current_hostname})'], "Committing VM changes", check=False)

run_command(["git", "push"], "Pushing to GitHub")

print("✅ VM state is now pushed to GitHub.")