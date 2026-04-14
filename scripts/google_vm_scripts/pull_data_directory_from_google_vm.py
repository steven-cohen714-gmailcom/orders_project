# File: scripts/pull_vm_data.py
# Purpose: Sync the remote `data/` directory to a specific local folder.

import subprocess
import os
import datetime
import shutil

# --- Configuration ---
VM_USER = "steven_cohen714"
VM_IP = "universalrecycling.co.za"

# VM project path and remote data dir on the VM
VM_PROJECT_PATH = f"/home/{VM_USER}/orders_project"
VM_DATA_DIR = os.path.join(VM_PROJECT_PATH, "data")  # full directory copy

# Local destination folder to sync to
LOCAL_DEST_DIR = "/Users/stevencohen/Projects/universal_recycling/orders_project/vm_data_backup"


# --- Pretty printing helpers ---
def print_header(text):   print(f"\n--- {text} ---")
def print_success(text):  print(f"✅ {text}")
def print_warning(text):  print(f"⚠️ {text}")
def print_error(text):    print(f"❌ {text}")

def run(command: str, check_return=True):
    """
    Run a shell command and stream output directly to the console.
    Returns True on success, False on failure (if check_return=False).
    """
    try:
        subprocess.run(command, check=check_return, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}: {e.cmd}")
        return False
    except FileNotFoundError:
        print_error(f"Command not found. Ensure '{command.split()[0]}' exists in PATH.")
        return False
    except Exception as e:
        print_error(f"Unexpected error running command: {e}")
        return False

def which(exe_name: str) -> bool:
    """Return True if an executable exists in PATH."""
    return shutil.which(exe_name) is not None

def summarize_dir(path: str):
    total_files = 0
    total_bytes = 0
    for root, _, files in os.walk(path):
        for f in files:
            total_files += 1
            try:
                total_bytes += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    print_success(f"Summary: {total_files} files, {total_bytes} bytes in '{path}'")

def main():
    print_header("Sync VM data directory")
    print(f"Remote: {VM_USER}@{VM_IP}:'{VM_DATA_DIR}/'")
    print(f"Local : '{LOCAL_DEST_DIR}'")

    # Ensure destination folder exists
    if not os.path.isdir(LOCAL_DEST_DIR):
        print_warning(f"Local destination path '{LOCAL_DEST_DIR}' does not exist. Creating…")
        try:
            os.makedirs(LOCAL_DEST_DIR, exist_ok=True)
            print_success(f"Created: '{LOCAL_DEST_DIR}'")
        except Exception as e:
            print_error(f"Failed to create destination directory: {e}")
            return

    # Prefer rsync (best practice)
    if which("rsync"):
        print_header("Using rsync (recommended for syncing)")
        # The `--delete` flag is crucial for syncing, as it removes files
        # from the destination that are no longer in the source.
        cmd = (
            f'rsync -avz --delete --progress '
            f'{VM_USER}@{VM_IP}:"{VM_DATA_DIR}/" '
            f'"{LOCAL_DEST_DIR}/"'
        )
        print(f"Running: {cmd}")
        ok = run(cmd, check_return=False)
    else:
        # Note: scp is a copy, not a true sync.
        # This will not remove files from the local directory that were
        # deleted from the remote.
        print_header("rsync not found — falling back to scp -r")
        cmd = (
            f'scp -p -r -v {VM_USER}@{VM_IP}:"{VM_DATA_DIR}" '
            f'"{LOCAL_DEST_DIR}"'
        )
        print(f"Running: {cmd}")
        ok = run(cmd, check_return=False)

    if not ok:
        print_error("Failed to sync the data directory from VM. Check SSH connectivity, paths, and permissions.")
        print_error(f"Verify the remote path exists:\n  {VM_USER}@{VM_IP}:{VM_DATA_DIR}")
        return

    # Post-copy verification
    print_header("Verifying local sync")
    if os.path.isdir(LOCAL_DEST_DIR):
        summarize_dir(LOCAL_DEST_DIR)
        print_success(f"Data synced to: {LOCAL_DEST_DIR}")
    else:
        print_error("Destination directory not found after transfer. Something went wrong.")

    print_header("Done")

if __name__ == "__main__":
    main()