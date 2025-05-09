#!/usr/bin/env python3

import subprocess
import socket

def run(cmd):
    return subprocess.run(cmd, check=False, capture_output=True, text=True)

hostname = socket.gethostname()

print("📥 Checking for local changes...")
status = run(["git", "status", "--porcelain"])
if status.stdout.strip():
    print("📦 Stashing local work...")
    run(["git", "stash", "push", "-u", "-m", f"Auto-stash from {hostname}"])

print("🔄 Pulling latest with rebase...")
run(["git", "pull", "--rebase", "origin", "main"])

stash_list = run(["git", "stash", "list"])
if f"Auto-stash from {hostname}" in stash_list.stdout:
    print("🔁 Re-applying stashed changes...")
    run(["git", "stash", "pop"])

print("✅ Ready to work.")
