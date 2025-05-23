#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

# --- Config ---
REMOTE_USER = "steven_cohen714"
REMOTE_IP = "34.35.73.12"
REMOTE_DB_PATH = "/home/steven_cohen714/orders_project/data/orders.db"
LOCAL_DEST = str(Path.home() / "Downloads/orders_vm.db")

def run_scp():
    print(f"⬇️  Copying DB from {REMOTE_USER}@{REMOTE_IP}...")
    result = subprocess.run(
        ["scp", f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_DB_PATH}", LOCAL_DEST],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ Downloaded DB to {LOCAL_DEST}")
    else:
        print(f"❌ Failed to download DB:\n{result.stderr.strip()}")
        sys.exit(1)

if __name__ == "__main__":
    run_scp()
