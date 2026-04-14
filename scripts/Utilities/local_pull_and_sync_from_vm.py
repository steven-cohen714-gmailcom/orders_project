# File: orders_project/scripts/Utilities/pull_and_sync_from_vm.py
# RUN THIS ON YOUR LOCAL MACHINE (MacBook/Mac Studio).
# Pulls the project's code from the VM's orders_project folder to the local project root.

import subprocess
import sys
import os
from pathlib import Path

# --- CONFIGURATION ---
REMOTE_USER = "steven_cohen714"
REMOTE_HOST = "universal-recycling-google-server"  # SSH host alias you use
REMOTE_PATH = "~/orders_project"                   # Remote folder to pull from
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
# Paths are relative to PROJECT_ROOT.
EXCLUDES = ["/venv/", "/data/", "/logs/", "/.git/", "/__pycache__/"]
EXCLUDE_ARGS = [f"--exclude={pat}" for pat in EXCLUDES]
PROTECT_ARGS = [f"--filter=protect {pat}" for pat in EXCLUDES]

def ensure_local_dir():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

def main():
    print(f"🔄 Pulling {REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}  →  {PROJECT_ROOT}")
    cmd = [
        "rsync",
        "-az",
        "--delete",
        "--stats", "-h",
        "-e", f"ssh -i {SSH_KEY} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new",
        *EXCLUDE_ARGS,
        *PROTECT_ARGS,
        f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}/",
        f"{PROJECT_ROOT.as_posix()}/",
    ]
    # Optional DRY RUN: run with DRY=1 env variable
    if os.environ.get("DRY") == "1":
        cmd.insert(1, "--dry-run")
        print("⚠️  DRY RUN enabled")

    try:
        ensure_local_dir()
        subprocess.run(cmd, check=True)
        print("✅ Pull sync complete.")
    except subprocess.CalledProcessError as e:
        print("❌ Pull sync failed:\n", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
