import subprocess
import os
import sys
import re
import difflib

# --- Configuration (Adjust if your paths or credentials change) ---
VM_USER = "steven_cohen714"
VM_IP = "34.35.73.12"

# Local project path will be determined dynamically
# Assumes this script is in: orders_project/scripts/google_vm_scripts/check_env.py
# We need to go up two levels to reach the 'orders_project' root from the script's location.
LOCAL_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

# VM project path is absolute
VM_PROJECT_PATH = f"/home/{VM_USER}/orders_project" # This should be consistent with your VM setup

REQ_FILE = "requirements.txt"
VENV_DIR_NAME = "venv" # Name of the virtual environment directory
SERVER_PORT = "8004"
APP_URL = f"http://{VM_IP}:{SERVER_PORT}/" # Main application URL

# --- Functions for consistent output ---
def print_header(text):
    print(f"\n--- {text} ---")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️ {text}")

def print_error(text):
    print(f"❌ {text}")

def run_local_command(command, shell=False, capture_output=True, text=True, timeout=10, error_message=""):
    try:
        result = subprocess.run(command, shell=shell, capture_output=capture_output, text=text, check=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if error_message:
            print_error(f"{error_message}: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        if error_message:
            print_error(f"{error_message}: Command not found.")
        return None
    except subprocess.TimeoutExpired:
        if error_message:
            print_error(f"{error_message}: Command timed out.")
        return None

def run_ssh_command(command_str, timeout=30, error_message=""):
    ssh_command = ["ssh", "-o", "ConnectTimeout=10", f"{VM_USER}@{VM_IP}", command_str]
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, check=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if error_message:
            print_error(f"{error_message}: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        if error_message:
            print_error(f"{error_message}: SSH client 'ssh' not found. Is OpenSSH client installed?")
        return None
    except subprocess.TimeoutExpired:
        if error_message:
            print_error(f"{error_message}: SSH command timed out. VM might be unresponsive or connection slow.")
        return None

# Normalize dependencies for comparison: remove comments, empty lines, and sort
def normalize_deps(deps_str):
    if not deps_str:
        return []
    lines = [line.split('#')[0].strip() for line in deps_str.splitlines()]
    return sorted([line for line in lines if line])

# --- Main Script Logic ---
def main():
    print("Starting Environment Consistency Check...")
    print(f"Local Project Root: {LOCAL_PROJECT_ROOT}")
    print(f"VM Project Path:    {VM_PROJECT_PATH}")
    print(f"VM IP:              {VM_IP}")
    print(f"Application URL:    {APP_URL}")

    # 0.5. Test Application Port Connectivity (Curl/Wget) - PRIORITIZED CHECK
    app_is_reachable = False
    print_header(f"Application Port Connectivity (Port {SERVER_PORT})")
    curl_command = ["curl", "--silent", "--output", "/dev/null", "--write-out", "%{http_code}", "--connect-timeout", "5", APP_URL]
    curl_output = run_local_command(curl_command, error_message=f"Curl to {APP_URL} failed")

    if curl_output == "200":
        print_success(f"Application responds on {APP_URL} (HTTP 200 OK).")
        app_is_reachable = True
    elif curl_output == "000":
        print_error(f"Application does NOT respond on {APP_URL} (Connection refused/timed out).")
        print_warning(f"This could mean: ")
        print_warning(f"  1. The VM's firewall (GCP) is blocking port {SERVER_PORT}.")
        print_warning(f"     -> ACTION: Check/create firewall rule for TCP:{SERVER_PORT} in GCP Console.")
        print_warning(f"  2. The application on the VM is NOT running or is listening on wrong IP/port.")
        print_warning(f"     -> ACTION: Check 'VM Server Process Status' below for details.")
    else:
        print_warning(f"Application responded with HTTP status '{curl_output}' or unexpected error.")
        print_warning(f"     -> This usually means the server is UP, but the application logic might have an error.")
        print_warning(f"     -> ACTION: Check VM logs for application errors.")
    
    if app_is_reachable:
        print_success("Application URL is reachable. Most critical network path is open.")
    else:
        print_error("Application URL is NOT reachable. Further network checks might be needed, or app is down.")

    # 0. Basic VM Connectivity Check (Ping) - SECONDARY CHECK
    print_header("Basic VM Connectivity (Ping)")
    ping_command = ["ping", "-c", "3", VM_IP]
    if sys.platform.startswith('win'):
        ping_command = ["ping", "-n", "3", VM_IP]

    ping_output = run_local_command(ping_command, error_message="Ping to VM failed")
    if ping_output and ("3 packets transmitted, 3 received" in ping_output or "Lost = 0" in ping_output):
        print_success(f"Ping to VM ({VM_IP}) successful.")
    else:
        if app_is_reachable: # If app is working but ping fails, it's just ICMP blocked
            print_warning(f"Ping to VM ({VM_IP}) failed, but application is reachable.")
            print_warning("This is usually normal for cloud VMs that block ICMP (ping) traffic by default.")
        else: # If app also failed, then ping failure is more significant
            print_error(f"Cannot ping VM ({VM_IP}).")
            print_error("This indicates a general network issue. Check VM status in GCP, your internet, or VPN/proxy settings.")
            # Do NOT sys.exit here, because we already did the curl check and want other diagnostic info


    # 1. Compare Python Versions
    print_header("Python Version Check")
    local_python_version = run_local_command([sys.executable, "--version"], error_message="Could not determine local Python version")
    if local_python_version:
        print_success(f"Local Python: {local_python_version}")
    else:
        local_python_version = "N/A"

    vm_python_version = None
    vm_venv_python_path = os.path.join(VM_PROJECT_PATH, VENV_DIR_NAME, "bin", "python")
    vm_python_version_cmd_venv = f'if [ -f "{vm_venv_python_path}" ]; then "{vm_venv_python_path}" --version; else echo ""; fi'
    vm_python_version = run_ssh_command(vm_python_version_cmd_venv, error_message="Could not determine VM Python version (venv)")

    if vm_python_version:
        print_success(f"VM Python (from venv): {vm_python_version}")
    else:
        vm_python_version_cmd_sys = f"python3 --version"
        vm_python_version = run_ssh_command(vm_python_version_cmd_sys, error_message="Could not determine VM Python version (system fallback)")
        if vm_python_version:
            print_warning(f"VM Python (system fallback): {vm_python_version}")
        else:
            print_error("VM Python version unknown. Is SSH configured? Is 'python3' in PATH on VM or venv active?")
            vm_python_version = "N/A"

    if local_python_version != "N/A" and vm_python_version != "N/A":
        local_v = re.search(r'\d+\.\d+\.\d+', local_python_version)
        vm_v = re.search(r'\d+\.\d+\.\d+', vm_python_version)
        if local_v and vm_v and local_v.group(0) == vm_v.group(0):
            print_success("Python versions match on Local and VM.")
        else:
            print_warning(f"Python versions DO NOT exactly match. Local: {local_python_version}, VM: {vm_python_version}")
            print_warning("ACTION: Consider updating the VM's Python version to match local for consistency.")
    else:
        print_warning(f"Cannot compare Python versions fully. Local: {local_python_version}, VM: {vm_python_version}")


    # 2. Compare Installed Python Dependencies
    print_header(f"Python Dependencies Check (vs. {REQ_FILE})")

    local_req_file = os.path.join(LOCAL_PROJECT_ROOT, REQ_FILE)
    local_venv_pip_path = os.path.join(LOCAL_PROJECT_ROOT, VENV_DIR_NAME, "bin", "pip")

    expected_deps = []
    if not os.path.exists(local_req_file):
        print_error(f"requirements.txt not found at {local_req_file}. Cannot perform dependency comparison.")
    else:
        with open(local_req_file, 'r') as f:
            requirements_content = f.read().strip()
        expected_deps = normalize_deps(requirements_content)
        print_success(f"requirements.txt found and processed.")


    local_pip_freeze = run_local_command([local_venv_pip_path, "freeze"], error_message=f"Local venv pip executable not found at {local_venv_pip_path}. Cannot check local dependencies.")
    if local_pip_freeze:
        print_success("Generated local pip freeze.")
    else:
        print_error("Failed to generate local pip freeze. Is your local venv active or path correct?")


    vm_pip_freeze = None
    vm_venv_activate_path = os.path.join(VM_PROJECT_PATH, VENV_DIR_NAME, "bin", "activate")
    vm_pip_freeze_cmd = f"""
    if [ -f "{vm_venv_activate_path}" ]; then
        source "{vm_venv_activate_path}" && pip freeze
    else
        echo "VM venv not found or activate script missing at {vm_venv_activate_path}." >&2
        exit 1
    fi
    """
    vm_pip_freeze_output = run_ssh_command(vm_pip_freeze_cmd, error_message="Failed to generate VM pip freeze")
    if vm_pip_freeze_output and not "VM venv not found" in vm_pip_freeze_output:
        vm_pip_freeze = vm_pip_freeze_output
        print_success("Generated VM pip freeze.")
    else:
        print_error(f"Failed to generate VM pip freeze. VM venv issue? Output: {vm_pip_freeze_output if vm_pip_freeze_output else 'No output.'}")


    if expected_deps: # Only compare if requirements.txt was found
        if local_pip_freeze:
            local_actual_deps = normalize_deps(local_pip_freeze)
            if local_actual_deps == expected_deps:
                print_success("Local dependencies exactly match requirements.txt.")
            else:
                print_warning("Local dependencies DO NOT exactly match requirements.txt. Differences found.")
                print("ACTION: Review local requirements. Run 'pip install -r requirements.txt' in your local venv.")
                diff_output = list(difflib.unified_diff(expected_deps, local_actual_deps, fromfile='requirements.txt', tofile='Local pip freeze', lineterm=''))
                if diff_output:
                    print("\n".join(diff_output))

        if vm_pip_freeze:
            vm_actual_deps = normalize_deps(vm_pip_freeze)
            if vm_actual_deps == expected_deps:
                print_success("VM dependencies exactly match requirements.txt.")
            else:
                print_warning("VM dependencies DO NOT exactly match requirements.txt. Differences found.")
                print_warning(f"ACTION: Sync VM dependencies: ssh {VM_USER}@{VM_IP} \"cd {VM_PROJECT_PATH} && source {VENV_DIR_NAME}/bin/activate && pip install -r {REQ_FILE}\"")
                diff_output = list(difflib.unified_diff(expected_deps, vm_actual_deps, fromfile='requirements.txt', tofile='VM pip freeze', lineterm=''))
                if diff_output:
                    print("\n".join(diff_output))
    else:
        print_warning("Skipping dependency comparison: requirements.txt not found.")


    # 3. Check Server Process Status on VM
    print_header(f"VM Server Process Status (Port {SERVER_PORT})")
    vm_process_status = run_ssh_command(f"sudo netstat -tulnp | grep :{SERVER_PORT}", error_message="Could not check VM process status")
    
    if vm_process_status and "LISTEN" in vm_process_status:
        match = re.search(r'LISTEN\s+(\d+)/(\S+)', vm_process_status)
        pid = match.group(1) if match else "N/A"
        process_name = match.group(2) if match else "N/A"
        print_success(f"Server is running on VM (Port {SERVER_PORT}) [PID: {pid}, Process: {process_name}].")
    else:
        print_error(f"Server is NOT running on VM (Port {SERVER_PORT}).")
        print_error("This is a CRITICAL application issue on the VM.")
        print_warning(f"ACTION: Try restarting the server on VM:")
        print_warning(f"        ssh {VM_USER}@{VM_IP} \"cd {VM_PROJECT_PATH} && source {VENV_DIR_NAME}/bin/activate && python3 scripts/stop_server.py && nohup python3 scripts/start_server.py &\"")
        print_warning(f"        After restarting, check the VM's application logs for errors (e.g., tail -f {VM_PROJECT_PATH}/logs/app.log).")


    print_header("Environment Check & Sync Script Complete")
    print("\n--- Summary & Next Steps ---")
    print("Review any ❌ (Error) or ⚠️ (Warning) messages above for recommended actions.")
    print("If all critical checks pass but the app is still not working, check the VM's application logs for errors:")
    print(f"  ssh {VM_USER}@{VM_IP} \"tail -f {VM_PROJECT_PATH}/logs/app.log\"")


if __name__ == "__main__":
    main()