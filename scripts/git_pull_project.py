#!/usr/bin/env python3

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
import shutil

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

def backup_database():
    db_file = Path("data/orders.db")
    if db_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = Path(f"data/orders_backup_{timestamp}.db")
        shutil.copy(db_file, backup_file)
        print(f"🗃️ Backed up database to {backup_file}")

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

    # Reset and backup DB
    db_file = "data/orders.db"
    db_path = Path(db_file)
    if db_path.exists():
        backup_database()
        print(f"🧹 Resetting database file: {db_file}")
        run(["git", "checkout", "--", db_file], f"Reset {db_file}", check=False)

    # Remove .pyc files
    print("🧹 Removing .pyc files...")
    subprocess.run(["find", ".", "-type", "f", "-name", "*.pyc", "-delete"], check=False)

def main():
    repo_path = Path(__file__).resolve().parents[1]
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📥 Git pull process starting...")

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

    # Reset untracked files before stashing
    reset_untracked_files()

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
        try:
            stash_result = run(["git", "stash", "pop"], "Restore stashed changes", check=False)
            if stash_result.returncode != 0:
                print("⚠️ Stash pop resulted in conflicts. Attempting to resolve...")
                conflict_result = run(["git", "status", "--porcelain"], "Check for conflicts")
                conflicts = [line for line in conflict_result.stdout.splitlines() if line.startswith("UU")]
                if conflicts:
                    print("🔍 Conflicts detected in:", conflicts)
                    for conflict in conflicts:
                        file_path = conflict.split(" ")[1]
                        if file_path.endswith(".pyc") or "logs/" in file_path or file_path == "data/orders.db":
                            print(f"🧹 Removing conflicting file: {file_path}")
                            run(["git", "rm", file_path], f"Remove {file_path}")
                        else:
                            print(f"🛠 Resolving conflict in {file_path} by keeping local version...")
                            run(["git", "checkout", "--ours", file_path], f"Resolve conflict in {file_path}")
                        run(["git", "add", file_path], f"Stage resolved {file_path}")
                    run(["git", "rebase", "--continue"], "Continue rebase after resolving conflicts")
                else:
                    print("⚠️ Stash pop failed for an unknown reason. Keeping local changes...")
        except SystemExit:
            print("⚠️ Stash pop failed, but local changes have been preserved.")

    # Final cleanup
    reset_untracked_files()
    print("✅ Git pull completed successfully!")

if __name__ == "__main__":
    main()
