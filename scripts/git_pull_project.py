#!/usr/bin/env python3

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
import shutil
import glob

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

def check_git_health():
    print("🔍 Checking Git repository health...")
    stat = shutil.disk_usage(".")
    free_space_mb = stat.free / (1024 * 1024)
    if free_space_mb < 100:
        print(f"⚠️ Low disk space: {free_space_mb:.2f} MB free.")
        sys.exit(1)

    git_dir = Path(".git")
    index_file = git_dir / "index"
    if not git_dir.exists():
        print("❌ .git directory not found.")
        sys.exit(1)

    if not os.access(git_dir, os.W_OK):
        print(f"❌ No write permissions for {git_dir}.")
        sys.exit(1)

    if index_file.exists() and not os.access(index_file, os.W_OK):
        print(f"❌ No write permissions for {index_file}.")
        sys.exit(1)

    if (git_dir / "index.lock").exists():
        print("⚠️ Git index is locked. Attempting to remove...")
        try:
            (git_dir / "index.lock").unlink()
            print("✅ Removed index.lock file.")
        except Exception as e:
            print(f"❌ Failed to remove index.lock: {e}")
            sys.exit(1)

def backup_database():
    db_file = Path("data/orders.db")
    if db_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = Path(f"data/orders_backup_{timestamp}.db")
        shutil.copy(db_file, backup_file)
        print(f"🗃️ Backed up database to {backup_file}")
        return backup_file
    return None

def clean_old_backups(keep_latest_n=3):
    print(f"🧹 Cleaning up old database backups (keeping latest {keep_latest_n})...")
    backup_files = sorted(glob.glob("data/orders_backup_*.db"), key=os.path.getmtime, reverse=True)
    if len(backup_files) > keep_latest_n:
        for old_backup in backup_files[keep_latest_n:]:
            print(f"🗑️ Removing old backup: {old_backup}")
            Path(old_backup).unlink()

def reset_untracked_files():
    print("🧹 Resetting untracked files to avoid conflicts...")
    logs_dir = Path("logs")
    if logs_dir.exists() and logs_dir.is_dir():
        for log_file in logs_dir.glob("*"):
            if log_file.is_file():
                print(f"🧹 Removing untracked log file: {log_file}")
                log_file.unlink()

    print("🧹 Removing .DS_Store files...")
    subprocess.run(["find", ".", "-type", "f", "-name", ".DS_Store", "-delete"], check=False)

    db_file = "data/orders.db"
    db_path = Path(db_file)
    if db_path.exists():
        backup_file = backup_database()
        print(f"🧹 Resetting database file: {db_file}")
        run(["git", "checkout", "--", db_file], f"Reset {db_file}", check=False)
        if backup_file:
            clean_old_backups(keep_latest_n=3)

    print("🧹 Removing .pyc files...")
    subprocess.run(["find", ".", "-type", "f", "-name", "*.pyc", "-delete"], check=False)

    individual_screens_path = Path("scripts/output_scripts_to_txt_files/Individual_screens")
    if individual_screens_path.exists():
        print(f"🧹 Removing outdated directory: {individual_screens_path}")
        shutil.rmtree(individual_screens_path)

def attempt_fix_index():
    print("⚠️ Git index issue detected. Attempting to fix...")
    index_file = Path(".git/index")
    if index_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        index_backup = Path(f".git/index_backup_{timestamp}")
        shutil.copy(index_file, index_backup)
        print(f"🗃️ Backed up Git index to {index_backup}")

    print("🧹 Resetting Git index...")
    run(["git", "reset"], "Reset Git index")
    print("✅ Git index reset successfully.")

def main():
    repo_path = Path(__file__).resolve().parents[1]
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📥 Git pull process starting...")
    check_git_health()

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

    reset_untracked_files()

    result = run(["git", "status", "--porcelain"], "Check for local changes")
    stashed = False

    if result.stdout.strip():
        print("📦 Local changes detected — stashing...")
        stash_result = run(["git", "stash", "push", "-u", "-m", "Auto-stash before pull"], "Create stash", check=False)
        if stash_result.returncode != 0 and "could not write index" in stash_result.stderr:
            attempt_fix_index()
            stash_result = run(["git", "stash", "push", "-u", "-m", "Auto-stash before pull (retry)"], "Retry create stash")
        stashed = True

    run(["git", "pull", "--rebase", "origin", "main"], "Pull latest changes with rebase")

    if stashed:
        print("🔁 Restoring stashed work...")
        try:
            stash_result = run(["git", "stash", "pop"], "Restore stashed changes", check=False)
            if stash_result.returncode != 0:
                print("⚠️ Stash pop resulted in conflicts. Attempting to resolve...")
                conflict_result = run(["git", "status", "--porcelain"], "Check for conflicts")
                conflicts = [line for line in conflict_result.stdout.splitlines() if line.startswith(("UU", "UD", "DU"))]
                if conflicts:
                    print("🔍 Conflicts detected in:", conflicts)
                    for conflict in conflicts:
                        file_path = conflict.split(" ")[-1]
                        conflict_type = conflict[:2]
                        if file_path.endswith(".pyc") or "__pycache__" in file_path:
                            print(f"🧹 Removing conflicting .pyc file: {file_path}")
                            run(["git", "rm", file_path], f"Remove {file_path}")
                        elif "logs/" in file_path:
                            if conflict_type == "DU":
                                print(f"🧹 Accepting upstream deletion for log file: {file_path}")
                                run(["git", "rm", file_path], f"Remove {file_path}")
                            else:
                                print(f"🧹 Resetting log file: {file_path}")
                                run(["git", "checkout", "--", file_path], f"Reset {file_path}", check=False)
                        elif file_path == "data/orders.db":
                            print(f"🧹 Resetting database file: {file_path}")
                            backup_database()
                            run(["git", "checkout", "--", file_path], f"Reset {file_path}", check=False)
                        else:
                            if conflict_type == "DU":
                                print(f"🧹 Accepting upstream deletion for file: {file_path}")
                                run(["git", "rm", file_path], f"Remove {file_path}")
                            elif conflict_type == "UD":
                                print(f"🧹 Accepting stashed deletion for file: {file_path}")
                                run(["git", "rm", file_path], f"Remove {file_path}")
                            else:
                                print(f"🛠 Resolving conflict in {file_path} by keeping local version...")
                                run(["git", "checkout", "--ours", file_path], f"Resolve conflict in {file_path}")
                            run(["git", "add", file_path], f"Stage resolved {file_path}")
                    run(["git", "rebase", "--continue"], "Continue rebase after resolving conflicts", check=False)
                else:
                    print("⚠️ Stash pop failed for an unknown reason. Keeping local changes...")
        except SystemExit:
            print("⚠️ Stash pop failed, but local changes have been preserved.")

    reset_untracked_files()
    print("✅ Git pull completed successfully!")

if __name__ == "__main__":
    main()