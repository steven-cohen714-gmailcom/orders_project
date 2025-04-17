#!/usr/bin/env python3
import os
import subprocess
import time
import shutil

# --- Configuration ---
PORT       = "8004"
LOG_PATH   = "logs/server.log"
APP_MODULE = "backend.main:app"   # run as `uvicorn backend.main:app`
# ----------------------

print("🟢 Starting FastAPI smart server (full cleanup)…")

# 1) Kill anything listening on PORT
print(f"🔪 Killing processes on port {PORT}…")
subprocess.run(f"lsof -ti:{PORT} | xargs kill -9", shell=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.5)
print(f"✅ Port {PORT} cleared.")

# 2) Remove all __pycache__ folders
print("🧹 Clearing Python bytecode caches…")
for root, dirs, _ in os.walk(".", topdown=True):
    if "__pycache__" in dirs:
        full = os.path.join(root, "__pycache__")
        try:
            shutil.rmtree(full)
            print(f"   • Removed {full}")
        except Exception:
            pass

# 3) Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# 4) Launch Uvicorn
print(f"🚀 Launching Uvicorn ({APP_MODULE}) on port {PORT}…")
with open(LOG_PATH, "a") as log_file:
    subprocess.Popen(
        ["uvicorn", APP_MODULE, "--host", "0.0.0.0", "--port", PORT, "--reload"],
        stdout=log_file,
        stderr=log_file,
        cwd=os.getcwd()  # must be project root so `backend` module is importable
    )

print(f"✅ Uvicorn launched. Logging → {LOG_PATH}")

