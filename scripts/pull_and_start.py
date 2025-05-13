#!/usr/bin/env python3

import subprocess
import socket
import sys

def run(cmd, desc=None, check=True):
    if desc:
        print(f"🔧 {desc}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error during: {desc or ' '.join(cmd)}")
        print(result.stderr.strip())
        sys.exit(1)
    return result

hostname = socket.gethostname()
stash_msg = f"Auto-stash from {hostname}"

print("📥 Checking for local changes...")
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

if status.stdout.strip():
    print("📦 Stashing local work...")
    run(["git", "stash", "push", "-u", "-m", stash_msg], "Stashing")

print("🔄 Pulling latest with rebase...")
run(["git", "pull", "--rebase", "origin", "main"], "Pulling from origin")

# Check if stash exists before popping
stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
if stash_msg in stash_list.stdout:
    print("🔁 Re-applying stashed changes...")
    run(["git", "stash", "pop"], "Stash pop")

print("✅ Ready to work.")
