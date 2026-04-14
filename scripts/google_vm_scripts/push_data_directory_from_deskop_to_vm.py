# File: push_data_directory_to_vm.py
# This script is intended to be RUN ON THE LOCAL MACHINE (Macbook/Mac Studio).
# It safely syncs the local 'data' directory on your Desktop to the VM's live project.

import subprocess
import sys
from pathlib import Path

# --- CONFIGURATION ---
# The path to the local data directory on your Desktop
LOCAL_DATA_DIR = Path.home() / "Desktop" / "data"

# The remote user, IP, and the destination path on the VM
REMOTE_USER = "steven_cohen714"
REMOTE_IP = "universalrecycling.co.za"
# The destination path on the VM.
REMOTE_DEST_DIR = f"/home/{REMOTE_USER}/orders_project/data/"

# The path to your SSH private key
SSH_KEY = (Path.home() / ".ssh" / "id_rsa").as_posix()

def ensure_remote_dir(remote_dir: str):
    """Creates the remote directory if it doesn't exist."""
    print(f"Ensuring remote directory {remote_dir} exists...")
    cmd = [
        "ssh",
        "-i", SSH_KEY,
        "-o", "IdentitiesOnly=yes",
        "-o", "StrictHostKeyChecking=accept-new",
        f"{REMOTE_USER}@{REMOTE_IP}",
        f"mkdir -p {remote_dir}",
    ]
    try:
        subprocess.run(cmd, check=True)
        print("✅ Remote directory is ready.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create remote directory:\n{e}")
        sys.exit(1)

def run_rsync():
    """Performs the recursive rsync command to copy the directory."""
    print(f"📤 Syncing local data directory to {REMOTE_USER}@{REMOTE_IP}...")
    
    # The rsync command with the -a (archive), -z (compress), and --delete flags.
    cmd = [
        "rsync",
        "-az",
        "--delete",
        "-e", f"ssh -i {SSH_KEY}",
        f"{LOCAL_DATA_DIR.as_posix()}/",
        f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_DEST_DIR}",
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Data directory synced successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to sync data directory:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    if not LOCAL_DATA_DIR.exists():
        print(f"❌ Local data directory not found at {LOCAL_DATA_DIR}")
        sys.exit(1)

    # First, make sure the destination directory exists on the VM
    ensure_remote_dir(REMOTE_DEST_DIR)

    # Then, run the rsync command to sync the files
    run_rsync()
