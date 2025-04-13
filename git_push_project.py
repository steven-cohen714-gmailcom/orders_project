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
    branch = "main"

    # Change to project directory
    try:
        os.chdir(project_dir)
    except FileNotFoundError:
        print(f"Error: Directory {project_dir} not found")
        sys.exit(1)

    print("📦 Starting Git push process...")

    # Stage everything (including untracked files)
    run_git_command(["git", "add", "--all"], "Failed to stage changes")

    # Check if anything is staged
    diff = run_git_command(["git", "diff", "--cached", "--name-only"], "Failed to check staged files")
    if not diff.strip():
        print("✅ Nothing to commit or push.")
        return

    # Commit the changes
    commit_msg = "Auto-commit for push (script)"
    run_git_command(["git", "commit", "-m", commit_msg], "Failed to commit changes")

    # Pull with rebase to avoid conflicts
    if run_git_command(["git", "pull", "--rebase", "origin", branch], "Pull failed") is None:
        print("❌ Pull failed. Resolve manually.")
        return

    # Push to GitHub
    if run_git_command(["git", "push", "origin", branch], "Push failed") is None:
        print("❌ Push failed. Resolve manually.")
        return

    print("🚀 Push completed successfully!")

if __name__ == "__main__":
    main()

