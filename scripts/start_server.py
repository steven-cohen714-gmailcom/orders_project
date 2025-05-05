#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

# --- CONFIG ---
PORT = "8004"
APP_MODULE = "backend.main:app"
LOG_FILE = "logs/server.log"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_UVICORN = PROJECT_ROOT / "venv/bin/uvicorn"
RELOAD_DIR = "backend"
# --------------

print("🟢 Starting FastAPI server...")

# 1. Ensure working directory and import paths
try:
    os.chdir(PROJECT_ROOT)
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    print(f"✅ Project root set: {PROJECT_ROOT}")
except Exception as e:
    print(f"❌ Failed to set project root: {e}")
    sys.exit(1)

# 2. Ensure uvicorn binary exists
if not VENV_UVICORN.exists():
    print(f"❌ Uvicorn not found at {VENV_UVICORN}")
    print("💡 Did you forget to create or activate your virtual environment?")
    sys.exit(1)

# 3. Kill any process using the port
print(f"🔪 Killing processes on port {PORT}...")
try:
    subprocess.run(f"lsof -ti:{PORT} | xargs kill -9", shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Port {PORT} cleared.")
except Exception as e:
    print(f"⚠️ Could not clear port {PORT}: {e}")

# 4. Remove all __pycache__ directories
print("🧹 Removing __pycache__ directories...")
try:
    for path in PROJECT_ROOT.rglob("__pycache__"):
        shutil.rmtree(path)
        print(f"   • Removed {path}")
    print("✅ Bytecode caches cleared.")
except Exception as e:
    print(f"⚠️ Failed to clean __pycache__ directories: {e}")

# 5. Ensure logs directory exists
try:
    os.makedirs("logs", exist_ok=True)
    print("✅ Logs directory ready.")
except Exception as e:
    print(f"⚠️ Could not create logs directory: {e}")

# 6. Start the server
print(f"🚀 Launching Uvicorn: {APP_MODULE} on port {PORT}...")
try:
    subprocess.Popen(
        f"{VENV_UVICORN} {APP_MODULE} --host 0.0.0.0 --port {PORT} --reload --reload-dir {RELOAD_DIR} >> {LOG_FILE} 2>&1",
        shell=True
    )
    print(f"✅ Server launched! Logs → {LOG_FILE}")
except Exception as e:
    print(f"❌ Failed to start server: {e}")
    sys.exit(1)
