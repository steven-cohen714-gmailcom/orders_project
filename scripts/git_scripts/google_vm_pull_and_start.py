#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run(cmd, desc=None, check=True):
    if desc:
        print(f"🔄 {desc}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error during: {desc or ' '.join(cmd)}")
        print(result.stderr.strip())
        sys.exit(1)
    return result

def kill_server():
    print("🛑 Checking for running server process...")
    result = subprocess.run(
        ["pgrep", "-f", "start_server.py"],
        capture_output=True,
        text=True
    )
    pids = result.stdout.strip().splitlines()
    if pids:
        for pid in pids:
            print(f"🔪 Killing server process with PID {pid}")
            subprocess.run(["kill", "-9", pid])
    else:
        print("✅ No server process found.")

# --- Config ---
db_path = Path("data/orders.db")
backup_path = Path(f"data/orders_db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

# --- Kill server if running ---
kill_server()

# --- Backup live DB ---
if db_path.exists():
    print(f"🧠 Backing up live DB → {backup_path.name}")
    db_path.replace(backup_path)

# --- Git sync ---
print("⚠️ VM: Wiping local changes — syncing clean from GitHub (excluding DB)...")
run(["git", "fetch", "origin"], "Fetching latest from origin")
run(["git", "reset", "--hard", "origin/main"], "Hard reset to remote main")
run(["git", "clean", "-fd"], "Removing untracked files and dirs")

# --- Restore DB ---
if backup_path.exists():
    print("♻️ Restoring live DB after Git pull")
    backup_path.replace(db_path)

print("✅ VM now EXACTLY matches GitHub — but live DB preserved.")
