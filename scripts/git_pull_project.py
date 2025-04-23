import subprocess
import os
import sys
from pathlib import Path

def run(command, desc):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr)
        sys.exit(1)

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📥 Git pull process starting...")

    # Check for local changes
    result = run(["git", "status", "--porcelain"], "Check for local changes")
    stashed = False

    if result.stdout.strip():
        print("📦 Local changes detected — stashing...")
        run(["git", "stash", "push", "-u", "-m", "Auto-stash before pull"], "Create stash")
        stashed = True

    # Pull with rebase
    run(["git", "pull", "--rebase", "origin", "main"], "Pull latest changes with rebase")

    # Restore stashed changes
    if stashed:
        print("🔁 Restoring stashed work...")

        # 🧹 Delete known log conflicts BEFORE popping stash
        conflict_logs = [
            "logs/db_activity_log.txt",
            "logs/server_startup.log"
        ]
        for log_file in conflict_logs:
            path = Path(log_file)
            if path.exists():
                print(f"🧹 Removing log file: {log_file}")
                path.unlink()

        # 🧹 Delete known .pyc cache file
        pycache_file = Path("backend/endpoints/__pycache__/orders.cpython-313.pyc")
        if pycache_file.exists():
            print(f"🧹 Removing pycache: {pycache_file}")
            pycache_file.unlink()

        try:
            run(["git", "stash", "pop"], "Restore stashed changes")
        except SystemExit:
            print("⚠️ Stash pop failed — resolve manually with `git stash list && git stash apply`")
            sys.exit(1)

    print("✅ Git pull completed successfully!")

if __name__ == "__main__":
    main()
