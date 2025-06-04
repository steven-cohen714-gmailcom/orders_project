# File: test_items_dropdown/start_test_item_server.py

import os
import subprocess
from pathlib import Path
import sys
import signal
import time

project_root = Path(__file__).resolve().parent.parent
venv_python = project_root / "venv" / "bin" / "python"
uvicorn_path = project_root / "venv" / "bin" / "uvicorn"

# Kill any uvicorn servers matching the test_items_dropdown app
subprocess.run("pkill -f 'uvicorn.*test_items_dropdown.app'", shell=True)

# Wait a sec to ensure it's dead
time.sleep(0.5)

# Start new server from the root
cmd = [
    str(uvicorn_path),
    "test_items_dropdown.app:app",
    "--reload",
    "--port", "8004"
]

print(f"\n🚀 Launching test_items_dropdown from: {project_root}\n")
subprocess.run(cmd, cwd=str(project_root))  # 👈 ensure correct launch context
