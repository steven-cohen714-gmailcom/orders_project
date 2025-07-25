import subprocess
import os
import datetime

# --- Configuration ---
VM_USER = "steven_cohen714"
VM_IP = "34.35.73.12"

# VM project path and database file path on the VM
VM_PROJECT_PATH = f"/home/{VM_USER}/orders_project"
VM_DB_RELATIVE_PATH = "data/orders.db"
VM_FULL_DB_PATH = os.path.join(VM_PROJECT_PATH, VM_DB_RELATIVE_PATH)

# Local destination path (your Desktop)
# This uses os.path.expanduser('~') for cross-platform home directory detection
LOCAL_DESKTOP_PATH = os.path.join(os.path.expanduser('~'), "Desktop")

# --- Functions for consistent output ---
def print_header(text):
    print(f"\n--- {text} ---")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️ {text}")

def print_error(text):
    print(f"❌ {text}")

def run_command(command, capture_output=False, check_return=True):
    """
    Runs a shell command and optionally captures output or checks for errors.
    """
    try:
        if capture_output:
            result = subprocess.run(command, capture_output=True, text=True, check=check_return, shell=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, check=check_return, shell=True)
            return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}: {e.cmd}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print_error(f"Command not found. Make sure '{command.split()[0]}' is in your PATH.")
        return False
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        return False

# --- Main Script Logic ---
def main():
    print_header("Pull VM Database Script")
    print(f"Source VM DB: {VM_USER}@{VM_IP}:{VM_FULL_DB_PATH}")
    print(f"Destination Local: {LOCAL_DESKTOP_PATH}")

    # Ensure the local Desktop directory exists
    if not os.path.exists(LOCAL_DESKTOP_PATH):
        print_warning(f"Local Desktop path '{LOCAL_DESKTOP_PATH}' does not exist. Attempting to create it.")
        try:
            os.makedirs(LOCAL_DESKTOP_PATH)
            print_success(f"Created directory: {LOCAL_DESKTOP_PATH}")
        except Exception as e:
            print_error(f"Failed to create Desktop directory: {e}")
            print_error("Cannot proceed without a valid local destination.")
            return

    # Construct the scp command
    # Use -p to preserve modification times, access times, and modes.
    # Use -v for verbose output (optional, but good for seeing progress)
    scp_command = f"scp -p -v {VM_USER}@{VM_IP}:{VM_FULL_DB_PATH} {LOCAL_DESKTOP_PATH}"

    print_header("Executing SCP Command")
    print(f"Running: {scp_command}")

    # Execute the scp command
    success = run_command(scp_command, capture_output=False, check_return=False) # Capture output here is true to show scp progress

    if success:
        pulled_file_path = os.path.join(LOCAL_DESKTOP_PATH, os.path.basename(VM_DB_RELATIVE_PATH))
        print_success(f"\n✅ Successfully copied '{os.path.basename(VM_DB_RELATIVE_PATH)}' from VM to {LOCAL_DESKTOP_PATH}")
        print(f"Local file path: {pulled_file_path}")

        # Optional: Verify file size (similar to check_env.py)
        if os.path.exists(pulled_file_path):
            local_pulled_db_size = os.path.getsize(pulled_file_path)
            print(f"Local pulled DB file size: {local_pulled_db_size} bytes")
        else:
            print_warning("Could not verify local pulled DB file size (file not found).")
    else:
        print_error("\n❌ Failed to copy database from VM. Please check error messages above.")
        print_error("Common issues: SSH connection problems, incorrect VM path, or file permissions on the VM.")
        print_error("Ensure you can SSH into the VM and the database file exists at:")
        print_error(f"  {VM_USER}@{VM_IP}:{VM_FULL_DB_PATH}")


    print_header("Script Complete")

if __name__ == "__main__":
    main()