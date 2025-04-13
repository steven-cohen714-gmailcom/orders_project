import subprocess
import os
from pathlib import Path
import sys

def run_git_command(args, error_msg):
    print(f"Running: {' '.join(args)}")
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_msg}")
        print(e.stderr)
        return None

def main():
    project_dir = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")

    # Navigate to the project directory
    try:
        os.chdir(project_dir)
    except FileNotFoundError:
        print(f"❌ Directory {project_dir} not found.")
        sys.exit(1)

    print("📥 Starting Git pull for Universal Recycling Purchase Orders...")

    # Check for any local changes (modified, staged, or untracked)
    status = run_git_command(["git", "status", "--porcelain"], "Failed to check git status")
    stashed = False

    if status.strip():
        print("📦 Local changes detected. Stashing (incl. untracked)...")
        run_git_command(["git", "stash", "push", "-u", "-m", "Auto-stash for pull"], "Failed to stash changes")
        stashed = True

    # Pull from origin with rebase
    print("🔄 Pulling latest from origin/main...")
    if run_git_command(["git", "pull", "--rebase", "origin", "main"], "Pull failed (conflict?)") is None:
        print("❗ Pull failed. Resolve conflicts manually.")
        if stashed:
            print("🔁 Attempting to restore stashed changes...")
            result = run_git_command(["git", "stash", "pop"], "Failed to pop stash")
            if result is None:
                print("⚠️  Stash pop failed. Run 'git stash show' and resolve manually.")
        sys.exit(1)

    if stashed:
        print("🔁 Restoring stashed changes...")
        result = run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
        if result is None:
            print("⚠️  Stash pop had conflicts. Run 'git stash show' and resolve manually.")

    print("✅ Pull completed successfully!")

if __name__ == "__main__":
    main()

