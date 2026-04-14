import sys
import os
import subprocess
import shutil
import platform

# --- Add project root to Python path ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, project_root)

# --- Imports (mobile/routers removed) ---
try:
    from backend.database import init_db
    from backend import main as backend_main
except ImportError as e:
    print(f"❌ ImportError: {e}")
    print("Ensure 'backend' directory exists and contains 'main.py' and 'database.py'.")
    sys.exit(1)

# --- Configuration ---
HOST = "0.0.0.0"
PORT = 8004
UVICORN_APP = "backend.main:app"
LOG_FILE = "logs/server.log"
VENV_PYTHON = sys.executable  # Use current Python interpreter
BACKEND_DIR = os.path.join(project_root, "backend")

print("🟢 Starting FastAPI server...")

# --- Ensure logs directory exists ---
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
print(f"✅ Logs directory ready at {logs_dir}")

# --- Verify backend directory ---
if not os.path.isdir(BACKEND_DIR):
    print(f"❌ Error: Backend directory not found at {BACKEND_DIR}")
    sys.exit(1)
print(f"✅ Using Python: {VENV_PYTHON}")

# --- Kill processes on port ---
print(f"🔪 Killing processes on port {PORT}...")
try:
    if platform.system() == "Darwin":  # macOS
        result = subprocess.run(
            f"lsof -iTCP:{PORT} -sTCP:LISTEN -t",
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            for pid in result.stdout.splitlines():
                print(f"  Killing process {pid} on port {PORT}...")
                subprocess.run(f"kill -9 {pid}", shell=True)
    else:  # Linux
        result = subprocess.run(
            f"lsof -iTCP:{PORT} -sTCP:LISTEN -t",
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            for pid in result.stdout.splitlines():
                print(f"  Killing process {pid} on port {PORT}...")
                subprocess.run(f"kill -9 {pid}", shell=True)
        else:
            # Fallback to ss/netstat
            result = subprocess.run(f"ss -tuln | grep :{PORT}", shell=True, capture_output=True, text=True)
            if not result.stdout:
                result = subprocess.run(f"netstat -tuln | grep :{PORT}", shell=True, capture_output=True, text=True)
            if result.stdout:
                result = subprocess.run(
                    f"lsof -iTCP:{PORT} -sTCP:LISTEN -t",
                    shell=True, capture_output=True, text=True
                )
                for pid in result.stdout.splitlines():
                    print(f"  Killing process {pid} on port {PORT}...")
                    subprocess.run(f"kill -9 {pid}", shell=True)
    print(f"✅ Port {PORT} cleared.")
except Exception as e:
    print(f"⚠️ Warning: Could not clear port {PORT}: {e}")

# --- Clear __pycache__ directories ---
print("🧹 Removing __pycache__ directories...")
for root, dirs, files in os.walk(project_root):
    if any(skip in root for skip in ("venv", ".git", "node_modules")):
        continue
    if "__pycache__" in dirs:
        target = os.path.join(root, "__pycache__")
        shutil.rmtree(target, ignore_errors=True)
        print(f"  • Removed {target}")
print("✅ Bytecode caches cleared.")

# --- Initialize Database ---
try:
    init_db()
    print("✅ Database initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize database: {e}")
    sys.exit(1)

# --- Audit registered routes ---
print("🧠 Auditing registered routes...")
try:
    app = backend_main.app
    route_audit_log_path = os.path.join(logs_dir, "route_audit.log")
    with open(route_audit_log_path, "w") as f:
        f.write("🔍 Registered Routes:\n")
        for route in app.routes:
            path = getattr(route, "path", "N/A")
            methods = ",".join(getattr(route, "methods", []) or []) or "N/A"
            name = getattr(route, "name", "N/A")
            f.write(f"{path} ({methods}) - {name}\n")
    print(f"✅ Route audit complete. Output → {route_audit_log_path}")
except Exception as e:
    print(f"⚠️ Warning: Could not audit routes: {e}")

# --- Launch Uvicorn Server ---
print(f"🚀 Launching Uvicorn: {UVICORN_APP} on port {PORT}...")
full_log_file_path = os.path.join(project_root, LOG_FILE)
uvicorn_command = (
    f"{VENV_PYTHON} -m uvicorn {UVICORN_APP} "
    f"--host {HOST} --port {PORT} --reload --reload-dir {BACKEND_DIR}"
)

try:
    os.chdir(project_root)
    print(f"✅ Changed working directory to {project_root}")
    with open(full_log_file_path, "w") as log_output:
        print(f"--- Uvicorn output will be redirected to {full_log_file_path} ---")
        subprocess.Popen(
            uvicorn_command,
            shell=True,
            stdout=log_output,
            stderr=log_output,
        )
    print(f"✅ Server launched! Check logs for Uvicorn output → {full_log_file_path}")
    print("This script will now exit, but the server will continue running.")
except Exception as e:
    print(f"❌ Failed to launch Uvicorn: {e}")
    sys.exit(1)
