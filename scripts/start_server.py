#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

# --- CONFIG ---
PORT = "8004"
APP_MODULE = "backend.main:app"  # <-- real FastAPI app location
LOG_FILE = "logs/server.log"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# --------------

print("🟢 Starting FastAPI server...")

# 1. Enforce project root and module importability
try:
    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, str(PROJECT_ROOT))
    print(f"✅ Changed working directory to project root: {PROJECT_ROOT}")
except Exception as e:
    print(f"❌ Failed to set project root: {e}")
    sys.exit(1)

# 2. Kill any process using the port
print(f"🔪 Killing any processes on port {PORT}...")
try:
    subprocess.run(f"lsof -ti:{PORT} | xargs kill -9", shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Port {PORT} cleared.")
except Exception as e:
    print(f"⚠️  Warning: Could not clear port {PORT}: {e}")

# 3. Remove all __pycache__ folders
print("🧹 Removing __pycache__ directories...")
try:
    for path in PROJECT_ROOT.rglob("__pycache__"):
        shutil.rmtree(path)
        print(f"   • Removed {path}")
    print("✅ Bytecode caches cleared.")
except Exception as e:
    print(f"⚠️  Warning: Failed to clean __pycache__ directories: {e}")

# 4. Ensure logs directory exists
try:
    os.makedirs("logs", exist_ok=True)
    print("✅ Logs directory ensured.")
except Exception as e:
    print(f"⚠️  Warning: Could not create logs directory: {e}")

# 5. Start Uvicorn with reload and persistent logging
print(f"🚀 Launching Uvicorn server → {APP_MODULE} on port {PORT}...")
try:
    subprocess.Popen(
        f"venv/bin/uvicorn {APP_MODULE} --host 0.0.0.0 --port {PORT} --reload --reload-dir backend >> {LOG_FILE} 2>&1",
        shell=True
    )
    print(f"✅ Server launched successfully! Logs → {LOG_FILE}")
except Exception as e:
    print(f"❌ Failed to launch Uvicorn: {e}")
    sys.exit(1)
