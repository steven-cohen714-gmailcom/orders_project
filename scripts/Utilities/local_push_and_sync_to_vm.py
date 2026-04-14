# File: push.py
# This script is intended to be RUN ON THE LOCAL MACHINE (Macbook/Mac Studio).
# It pushes the project's code to the VM's staging folder (sync_folder).

import subprocess
import sys
import os
from pathlib import Path

# --- CONFIGURATION ---
REMOTE_USER = "steven_cohen714"
REMOTE_IP = "universalrecycling.co.za"
# The remote staging folder that lives OUTSIDE the project on the VM
REMOTE_PATH = "~/sync_folder"
SSH_KEY = (Path.home() / ".ssh" / "id_rsa").as_posix()

def find_project_root(start: Path) -> Path:
    p = start.resolve()
    while True:
        if (p / "backend").is_dir() and (p / "frontend").is_dir():
            return p
        if p.parent == p:
            print("❌ Could not locate project root (need 'backend' and 'frontend' folders).", file=sys.stderr)
            sys.exit(1)
        p = p.parent

PROJECT_ROOT = find_project_root(Path(__file__))

# These folders are local to each machine and should NEVER be synced.
# Since data and logs are inside the project now, we exclude them.
EXCLUDES = ["/venv/", "/data/", "/logs/", "/.git/", "/__pycache__/"]
EXCLUDE_ARGS = [f"--exclude={pat}" for pat in EXCLUDES]
PROTECT_ARGS = [f"--filter=protect {pat}" for pat in EXCLUDES]

def ensure_remote_dir():
    cmd = [
        "ssh",
        "-i", SSH_KEY,
        "-o", "IdentitiesOnly=yes",
        "-o", "StrictHostKeyChecking=accept-new",
        f"{REMOTE_USER}@{REMOTE_IP}",
        f"mkdir -p {REMOTE_PATH}",
    ]
    subprocess.run(cmd, check=True)

def main():
    print(f"🔄 Pushing {PROJECT_ROOT}  →  {REMOTE_USER}@{REMOTE_IP}:{REMOTE_PATH}")
    cmd = [
        "rsync",
        "-az",
        "--delete",
        "--stats", "-h",
        "-e", f"ssh -i {SSH_KEY} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new",
        *EXCLUDE_ARGS,
        *PROTECT_ARGS,
        f"{PROJECT_ROOT.as_posix()}/",
        f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_PATH}/",
    ]
    if os.environ.get("DRY") == "1":
        cmd.insert(1, "--dry-run")
        print("⚠️  DRY RUN enabled")

    try:
        ensure_remote_dir()
        subprocess.run(cmd, check=True)
        print("✅ Push sync complete.")
    except subprocess.CalledProcessError as e:
        print("❌ Push sync failed:\n", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
