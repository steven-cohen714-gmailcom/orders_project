import subprocess
import os

def check_port(port):
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout == ""
    except Exception as e:
        print(f"Error checking port {port}: {e}")
        return False

def start_server():
    port = 8004

    if check_port(port):
        print(f"✅ Starting FastAPI server on port {port}...")
        os.system("uvicorn backend.main:app --host 0.0.0.0 --port 8004 --reload > uvicorn.log 2>&1 &")
        print("🪵 Server is starting. Now tailing the log (CTRL+C to stop watching):")
    else:
        print(f"❌ Port {port} is already in use. Please close the application using this port and try again.")

if __name__ == "__main__":
    start_server()

