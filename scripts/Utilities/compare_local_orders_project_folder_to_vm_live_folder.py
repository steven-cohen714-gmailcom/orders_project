# File: compare_local_to_live.py
# This script compares the local project to the VM's live project directory.
# It uses a dry run to show differences without making any changes.

import subprocess
import sys
import os
from pathlib import Path

# --- CONFIGURATION ---
REMOTE_USER = "steven_cohen714"
REMOTE_IP   = "universalrecycling.co.za"
REMOTE_PATH = "~/orders_project"
SSH_KEY     = (Path.home() / ".ssh" / "id_rsa").as_posix()

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
EXCLUDES = ["/venv/", "/data/", "/logs/", "/.git/", "/__pycache__/"]
EXCLUDE_ARGS = [f"--exclude={pat}" for pat in EXCLUDES]

def main():
    print(f"🔎 Comparing local project to VM's live project (DRY RUN)")
    cmd = [
        "rsync",
        "-az",
        "--dry-run",
        "--delete",
        "-e", f"ssh -i {SSH_KEY} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new",
        *EXCLUDE_ARGS,
        f"{PROJECT_ROOT.as_posix()}/",
        f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_PATH}/",
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Comparison complete. The above list shows the changes a 'push' would make to the live project.")
    except subprocess.CalledProcessError as e:
        print("❌ Comparison failed:\n", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
