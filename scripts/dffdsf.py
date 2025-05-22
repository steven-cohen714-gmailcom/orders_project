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

print("🧠 Staging and committing all VM project files...")
run(["git", "add", "-A"], "Staging ALL files")
run(["git", "commit", "-m", f'SYNC FROM VM ({hostname})'], "Committing VM changes", check=False)
run(["git", "push"], "Pushing to GitHub")

print("✅ VM state is now pushed to GitHub.")
