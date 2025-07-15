#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

# --- Config ---
LOCAL_DB_PATH = Path("data/orders.db")  # Adjust if your DB is somewhere else
REMOTE_USER = "steven_cohen714"
REMOTE_IP = "34.35.73.12"
REMOTE_DEST = "/home/steven_cohen714/orders_project/data/orders_from_mac.db"  # ⬅️ Safe name

def run_scp():
    print(f"📤 Uploading local DB to {REMOTE_USER}@{REMOTE_IP}...")
    result = subprocess.run(
        ["scp", str(LOCAL_DB_PATH), f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_DEST}"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ Uploaded DB as {REMOTE_DEST} (manually rename if needed)")
    else:
        print(f"❌ Failed to upload DB:\n{result.stderr.strip()}")
        sys.exit(1)

if __name__ == "__main__":
    if not LOCAL_DB_PATH.exists():
        print(f"❌ Local DB not found at {LOCAL_DB_PATH}")
        sys.exit(1)
    run_scp()
