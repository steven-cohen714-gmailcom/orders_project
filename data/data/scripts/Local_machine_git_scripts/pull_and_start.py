#!/usr/bin/env python3

import subprocess
import sys

def run(cmd, desc=None, check=True):
    if desc:
        print(f"🔄 {desc}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error during: {desc or ' '.join(cmd)}")
        print(result.stderr.strip())
        sys.exit(1)
    return result

print("⚠️ Wiping local changes — hard reset to match GitHub...")
run(["git", "fetch", "origin"], "Fetching latest from origin")
run(["git", "reset", "--hard", "origin/main"], "Hard reset to remote main")
run(["git", "clean", "-fd"], "Removing untracked files and dirs")

print("✅ MacBook now EXACTLY matches GitHub — fully synced.")
