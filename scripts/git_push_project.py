import subprocess
import os
import sys
from pathlib import Path

def run(command, desc, check=True):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr)
        if check:
            sys.exit(1)
        return e

def reset_untracked_files():
    print("🧹 Resetting untracked files to avoid conflicts...")
    # Reset log files
    conflict_files = [
        "logs/db_activity_log.txt",
        "logs/server_startup.log",
        "logs/server.log",
        "logs/new_orders_log.txt",
        "logs/twilio.log",
        "logs/whatsapp_log.txt",
    ]
    for log_file in conflict_files:
        path = Path(log_file)
        if path.exists():
            print(f"🧹 Resetting log file: {log_file}")
            run(["git", "checkout", "--", log_file], f"Reset {log_file}", check=False)

    # Reset database file
    db_file = "data/orders.db"
    db_path = Path(db_file)
    if db_path.exists():
        print(f"🧹 Resetting database file: {db_file}")
        run(["git", "checkout", "--", db_file], f"Reset {db_file}", check=False)

    # Remove .pyc files
    print("🧹 Removing .pyc files...")
    subprocess.run(["find", ".", "-type", "f", "-name", "*.pyc", "-delete"], check=False)

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📤 Git push process starting...")

    # Check if Git is in a conflicted state
    status_result = run(["git", "status", "--porcelain"], "Check Git status")
    conflicts = [line for line in status_result.stdout.splitlines() if line.startswith("UU")]
    if conflicts:
        print("🔍 Conflicts detected:", conflicts)
        for conflict in conflicts:
            file_path = conflict.split(" ")[1]
            print(f"🛠 Resolving conflict in {file_path} by removing from index...")
            run(["git", "rm", file_path], f"Remove {file_path} from index")
        print("🛠 Completing any interrupted operations...")
        run(["git", "rebase", "--continue"], "Continue rebase", check=False)
        run(["git", "merge", "--continue"], "Continue merge", check=False)
        run(["git", "reset"], "Reset index")

    # Reset untracked files before committing
    reset_untracked_files()

    # Check for local changes
    result = run(["git", "status", "--porcelain"], "Check for local changes")
    if not result.stdout.strip():
        print("✅ No changes to commit. Repository is clean.")
        return

    # Stage all changes
    run(["git", "add", "."], "Stage all changes")

    # Commit changes
    run(["git", "commit", "-m", "Auto-commit by git_push_project.py"], "Commit changes")

    # Push to origin/main
    run(["git", "push", "origin", "main"], "Push to origin/main")

    # Final cleanup of untracked files
    reset_untracked_files()

    print("✅ Git push completed successfully!")

if __name__ == "__main__":
    main()