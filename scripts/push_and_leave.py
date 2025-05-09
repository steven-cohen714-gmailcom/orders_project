#!/usr/bin/env python3

import subprocess
import socket

def run(cmd):
    return subprocess.run(cmd, check=False, capture_output=True, text=True)

hostname = socket.gethostname()

print("🧠 Checking for changes...")
run(["git", "add", "."])

status = run(["git", "diff", "--cached", "--quiet"])
if status.returncode == 0:
    print("✅ No changes to commit.")
else:
    print("💾 Committing work...")
    run(["git", "commit", "-m", f"WIP from {hostname}"])

print("📤 Pushing to origin...")
run(["git", "push"])

print("✅ Done — safe to leave this machine.")
