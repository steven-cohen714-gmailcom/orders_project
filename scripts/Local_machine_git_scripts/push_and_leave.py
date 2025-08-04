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

print("🧠 Force-staging EVERYTHING including deletions...")
run(["git", "add", "-A"], "Staging all files (including deletions)")

print("💾 Forcing commit of ALL files...")
run(["git", "commit", "-m", f'FULL SYNC from {hostname}'], "Committing", check=False)

print("📤 Force pushing to GitHub (replaces remote)...")
run(["git", "push", "--force"], "Force push")

print("✅ Studio state is now live on GitHub — full replacement.")
