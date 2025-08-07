import subprocess
import os
import sys
from pathlib import Path
import shutil

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# UVICORN_APP and HOST/PORT are no longer directly used for starting the server in this script
# UVICORN_APP = "backend.main:app"
# HOST = "0.0.0.0"
# PORT = 8004

def run_command(cmd, desc=None, check=True):
    """
    Runs a shell command and checks for errors.
    """
    if desc:
        print(f"🔧 {desc}")
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, check=check)
    
    # If check is True and the command failed, print stderr and exit
    if check and result.returncode != 0:
        print(f"❌ Error during: {desc or ' '.join(cmd)}")
        print("--- STDOUT ---")
        print(result.stdout.strip())
        print("--- STDERR ---")
        print(result.stderr.strip())
        sys.exit(1)
    # If check is False and the command failed, just print stderr as a warning
    elif not check and result.returncode != 0:
        print(f"⚠️ Warning during: {desc or ' '.join(cmd)}")
        print("--- STDOUT ---")
        print(result.stdout.strip())
        print("--- STDERR ---")
        print(result.stderr.strip())

    return result

# The kill_processes_on_port function is no longer needed if the server isn't started by this script.
# Keeping it commented out for reference in case you want to re-add server starting later.
# def kill_processes_on_port(port):
#     """
#     Finds and kills any processes listening on the given port.
#     This function uses 'lsof' to find PIDs and 'kill -9' to terminate them.
#     """
#     print(f"🔄 Checking for processes on port {port}...")
#     try:
#         # Find PIDs listening on the port. Use '-t' for PIDs only.
#         find_process_cmd = ["lsof", "-t", "-i", f"tcp:{port}"]
#         pids_result = subprocess.run(find_process_cmd, capture_output=True, text=True, check=False) # check=False because lsof returns 1 if no process found

#         pids = pids_result.stdout.strip().split('\n')
#         pids = [pid for pid in pids if pid] # Filter out empty strings

#         if not pids: # If the list is empty after filtering
#             print(f"✅ No processes found on port {port}.")
#             return

#         for pid in pids:
#             print(f"🔧 Found process with PID {pid} on port {port}. Killing it...")
#             try:
#                 subprocess.run(["kill", "-9", pid], check=True)
#                 print(f"✅ Process {pid} killed successfully.")
#             except subprocess.CalledProcessError as e:
#                 print(f"❌ Failed to kill process {pid}: {e.stderr.strip()}")
#             except Exception as e:
#                 print(f"❌ An unexpected error occurred while killing PID {pid}: {e}")

#     except Exception as e:
#         print(f"❌ An error occurred while trying to find processes on port {port}: {e}")
#         # You might want to exit here if it's a critical error,
#         # but for port killing, it might be recoverable.

def create_gitignore_file():
    """
    Ensures a .gitignore exists and contains necessary entries.
    """
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("venv/\n")
            f.write("logs/\n")
            f.write("data/\n")
            f.write(".DS_Store\n")
            f.write("__pycache__/\n")
        print("✅ .gitignore file created.")
    
def main():
    print(f"🚀 Starting fresh deployment process on local machine...")
    
    # 1. Ensure .gitignore is set up correctly
    create_gitignore_file()

    # 2. Clean and pull latest from GitHub
    print("🔄 Pulling latest changes from GitHub...")
    run_command(["git", "fetch", "origin"], "Fetching changes")
    run_command(["git", "reset", "--hard", "origin/main"], "Overwriting local files to match GitHub")

    # 3. Re-create virtual environment and install dependencies
    print("🔄 Re-creating virtual environment and installing dependencies...")
    venv_dir = PROJECT_ROOT / "venv"
    if venv_dir.exists():
        run_command(["rm", "-rf", str(venv_dir)], "Deleting old virtual environment")
    
    run_command([sys.executable, "-m", "venv", "venv"], "Creating new virtual environment")
    run_command(["./venv/bin/pip", "install", "-r", "requirements.txt"], "Installing dependencies")
    print("✅ Environment setup and dependency installation complete.")

    # Server is no longer started by this script.
    print("✨ Pull and environment setup process finished. The server was NOT automatically started.")

if __name__ == "__main__":
    main()
