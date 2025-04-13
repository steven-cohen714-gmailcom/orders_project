import os
import subprocess
from pathlib import Path

project_dir = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
venv_activate = project_dir / "venv/bin/activate"
log_file = project_dir / "uvicorn.log"

# Build the command to run in the background
command = f"cd {project_dir} && source {venv_activate} && uvicorn backend.main:app --host 0.0.0.0 --port 8004 --reload > {log_file} 2>&1 &"

print("🚀 Starting Uvicorn server in background...")
subprocess.run(command, shell=True, executable="/bin/bash")
print(f"✅ Server running. Logs → {log_file}")
