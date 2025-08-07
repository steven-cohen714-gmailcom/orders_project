import subprocess
import os
import sys
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def run_command(cmd, desc=None, check=True):
    """
    Runs a shell command and checks for errors.
    If check is True and command fails, prints error and exits.
    If check is False and command fails, prints warning.
    """
    if desc:
        print(f"🔧 {desc}")
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, check=False) # Always capture output, handle check manually
    
    if result.returncode != 0:
        error_type = "❌ Error" if check else "⚠️ Warning"
        print(f"{error_type} during: {desc or ' '.join(cmd)}")
        print("--- STDOUT ---")
        print(result.stdout.strip())
        print("--- STDERR ---")
        print(result.stderr.strip())
        if check:
            sys.exit(1) # Exit only if check is True and command failed
    
    return result

def create_and_manage_gitignore():
    """
    Ensures a .gitignore exists and contains necessary entries for ignored files.
    Also ensures these files/directories are untracked from Git's index.
    """
    gitignore_path = PROJECT_ROOT / ".gitignore"
    ignored_entries = [
        "venv/",
        "logs/",
        "data/", # Explicitly ignore the data directory (where your DB is)
        ".DS_Store",
        "__pycache__/",
        "*.pyc", # Ignore compiled Python files
        "*.sqlite3", # Specific for SQLite databases if not in data/
        "*.db", # Generic database files
        "*.log", # Generic log files
        "*.tmp", # Temporary files
        "*.bak", # Backup files
        "*.swp", # Vim swap files
        "*.swo", # Vim swap files
        "*.swn", # Vim swap files
    ]

    print("🔧 Ensuring .gitignore is set up correctly and untracking specific files...")

    # Read existing .gitignore content
    existing_content = []
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            existing_content = f.read().splitlines()

    # Add missing entries
    updated_content = list(existing_content)
    for entry in ignored_entries:
        if entry not in updated_content:
            updated_content.append(entry)

    # Write back the updated .gitignore
    with open(gitignore_path, "w") as f:
        for line in updated_content:
            f.write(line + "\n")
    
    print("✅ .gitignore file updated with necessary exclusions.")

    # Ensure ignored directories are not tracked by Git (important for 'data/')
    # Use check=False because 'git rm --cached' will fail if the file/dir isn't tracked,
    # which is the desired state.
    run_command(["git", "rm", "-r", "--cached", "data"], "Untracking 'data/' directory from Git index", check=False)
    run_command(["git", "rm", "-r", "--cached", "logs"], "Untracking 'logs/' directory from Git index", check=False)
    run_command(["git", "rm", "-r", "--cached", "venv"], "Untracking 'venv/' directory from Git index", check=False)
    print("✅ Ensured 'data/', 'logs/', and 'venv/' are untracked by Git.")


def main():
    print("🚀 Starting force sync to GitHub (acting as backup)...")
    
    # 1. Ensure .gitignore is set up correctly and untrack unwanted files
    create_and_manage_gitignore()
    
    # 2. Stage all changes (except ignored ones)
    run_command(["git", "add", "-A"], "Staging all files (except ignored ones)")
    
    # 3. Create a commit
    # Use check=False for commit in case there are no changes to commit.
    commit_message = "Automated force sync from local machine"
    run_command(["git", "commit", "-m", commit_message], "Committing changes", check=False)

    # 4. Perform a force push (overwrites remote history)
    print("\n⚠️ WARNING: This will overwrite the state of the 'main' branch on GitHub.")
    print("This is the 'backup' you asked for.")
    confirmation = input("Do you want to continue with the force push? (yes/no): ")
    if confirmation.lower() == 'yes':
        run_command(["git", "push", "--force"], "Overwriting remote with local state")
        print("\n✨ Force sync complete. GitHub repository is now an exact copy of your local code (excluding ignored files).")
        print("You can now safely run 'pull_and_start.py' on your other machines.")
    else:
        print("\n❌ Push cancelled. No changes were made to the remote repository.")
        sys.exit(0)

if __name__ == "__main__":
    main()
