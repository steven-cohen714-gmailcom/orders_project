#!/usr/bin/env python3

"""
Pushes the local orders.db to the Universal Recycling production VM using scp.

✔ Portable — uses relative project structure to locate the DB
✔ Safe — checks for existence before pushing
✔ SSH Config Friendly — uses alias 'universal-vm' from ~/.ssh/config

Target VM:
- Alias: universal-vm
- Defined in ~/.ssh/config
- Remote path: ~/orders_project/data/orders.db
"""

import subprocess
from pathlib import Path

# --- Config ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCAL_DB_PATH = PROJECT_ROOT / "data" / "orders.db"
REMOTE_HOST_ALIAS = "universal-vm"  # Uses your ~/.ssh/config
REMOTE_PATH = "~/orders_project/data/orders.db"

# --- Push DB ---
def push_db():
    if not LOCAL_DB_PATH.exists():
        print(f"❌ Local DB not found at: {LOCAL_DB_PATH}")
        return

    print(f"📤 Copying DB from:\n  {LOCAL_DB_PATH}\nto:\n  {REMOTE_HOST_ALIAS}:{REMOTE_PATH}")
    try:
        subprocess.run(
            ["scp", str(LOCAL_DB_PATH), f"{REMOTE_HOST_ALIAS}:{REMOTE_PATH}"],
            check=True
        )
        print("✅ DB successfully copied to VM.")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to copy DB:", e)

if __name__ == "__main__":
    push_db()
