#!/usr/bin/env python3
import subprocess

def kill_matching(pattern):
    try:
        result = subprocess.run(
            f"pgrep -f '{pattern}'",
            shell=True,
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip().splitlines()
        if not pids:
            print(f"ℹ️ No process found matching: {pattern}")
            return

        for pid in pids:
            subprocess.run(["kill", "-9", pid])
            print(f"🛑 Killed PID {pid} matching '{pattern}'")
    except Exception as e:
        print(f"⚠️ Error killing '{pattern}': {e}")

print("🛑 Stopping any lingering Uvicorn or FastAPI server processes...")
kill_matching("uvicorn")
kill_matching("start_server.py")
print("✅ Server fully stopped.")
