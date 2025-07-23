# File: /Users/stevencohen/Projects/universal_recycling/orders_project/scripts/start_server.py

import sys
import os
import subprocess
import time
import shutil

# --- FIX START: Add project root to Python path ---
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root (one level up from 'scripts')
project_root = os.path.dirname(script_dir)
# Add project root to sys.path so 'backend' can be imported
sys.path.insert(0, project_root)
# --- FIX END ---

# Now, imports like 'backend.database' should work
from backend.database import get_db_connection # This import should now succeed
from backend.endpoints import routers # Assuming this is used for audit
from backend.endpoints.mobile import mobile_awaiting_authorisation # Assuming this is the router for filtering

# --- Configuration ---
HOST = "0.0.0.0"
PORT = 8004
UVICORN_APP = "backend.main:app"
LOG_FILE = "logs/server.log"
# --- End Configuration ---

print("🟢 Starting FastAPI server...")

# --- Ensure logs directory exists ---
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
print(f"✅ Logs directory ready.")

# --- Kill processes on the port ---
print(f"🔪 Killing processes on port {PORT}...")
try:
    # Find process using the port (macOS/Linux)
    lsof_command = f"lsof -iTCP:{PORT} -sTCP:LISTEN"
    result = subprocess.run(lsof_command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        lines = result.stdout.splitlines()
        if len(lines) > 1: # Skip header line
            for line in lines[1:]:
                pid = line.split()[1] # PID is the second column
                print(f"  Killing process {pid} on port {PORT}...")
                subprocess.run(f"kill -9 {pid}", shell=True) # Force kill
    print(f"✅ Port {PORT} cleared.")
except Exception as e:
    print(f"⚠️ Warning: Could not clear port {PORT}. It might still be in use: {e}")
    # Continue execution, but user might need to manually kill if error persists

# --- Clear __pycache__ directories ---
print("🧹 Removing __pycache__ directories (excluding venv)...")
for root, dirs, files in os.walk(project_root):
    if "venv" in root or ".git" in root or "node_modules" in root:
        continue
    if "__pycache__" in dirs:
        shutil.rmtree(os.path.join(root, "__pycache__"))
        print(f"  • Removed {os.path.join(root, '__pycache__')}")
print("✅ Bytecode caches cleared.")

# --- Initialize Database ---
try:
    # This call now works because project_root is in sys.path
    from backend.database import init_db
    init_db()
    print("✅ Database initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize database: {e}")
    print("Please ensure your database setup is correct. Server may not start.")
    # Exit or re-raise if DB is critical for server start

# --- Audit registered routes (optional, but good for debugging) ---
print("🧠 Auditing registered routes...")
try:
    # Importing main.py which defines the FastAPI app and includes all routers
    from backend import main as backend_main
    app = backend_main.app # Get the FastAPI app instance

    route_audit_log_path = os.path.join(logs_dir, "route_audit.log")
    with open(route_audit_log_path, "w") as f:
        f.write("🔍 Registered Routes:\n")
        for route in app.routes:
            # Check if route has path and methods attributes
            path = getattr(route, 'path', 'N/A')
            methods = ','.join(getattr(route, 'methods', ['N/A'])) if getattr(route, 'methods', None) else 'N/A'
            name = getattr(route, 'name', 'N/A') # Or route.name for Route
            
            f.write(f"{path} ({methods}) - {name}\n")

    print("✅ Route audit complete. Output → logs/route_audit.log")
except Exception as e:
    print(f"⚠️ Warning: Could not audit routes: {e}")


# --- Launch Uvicorn Server ---
print(f"🚀 Launching Uvicorn: {UVICORN_APP} on port {PORT}...")
# Removed output redirection for immediate debugging in console
uvicorn_command = f"{sys.executable} -m uvicorn {UVICORN_APP} --host {HOST} --port {PORT} --reload --reload-dir backend"
try:
    # Use Popen to run Uvicorn in a non-blocking way, so the script can finish
    # The Uvicorn process will continue running in the background (or foreground if terminal stays open)
    # This also helps ensure its output is visible directly in the terminal for debugging
    # The user can then press Ctrl+C to stop Uvicorn.
    print("--- Uvicorn output will appear below. Press CTRL+C to stop the server ---")
    subprocess.Popen(uvicorn_command, shell=True) # Popen allows the script to continue
    print(f"✅ Server launched! Logs (if configured by Uvicorn) → {LOG_FILE}")
except Exception as e:
    print(f"❌ Failed to launch Uvicorn: {e}")
    print("Please check your Uvicorn command and Python environment.")