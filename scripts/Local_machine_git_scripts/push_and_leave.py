#orders_project/scripts/Local_machine_git_scripts/push_and_leave.py

import subprocess
import os
import sys
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def run_command(cmd, desc=None, check=True):
    """
    Runs a shell command and checks for errors.
    """
    if desc:
        print(f"🔧 {desc}")
    
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, check=check)
    
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)
    
    return result

def create_gitignore_file():
    """
    Ensures a .gitignore exists and contains necessary entries.
    """
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        print("🔧 Creating .gitignore file...")
        with open(gitignore_path, "w") as f:
            f.write("venv/\n")
            f.write("logs/\n")
            f.write("data/\n")
            f.write(".DS_Store\n")
            f.write("__pycache__/\n")
        print("✅ .gitignore file created with necessary exclusions.")

def main():
    print("🚀 Starting force sync to GitHub...")
    
    # 1. Ensure .gitignore is set up correctly
    create_gitignore_file()
    
    # 2. Stage all changes
    run_command(["git", "add", "-A"], "Staging all files (except ignored ones)")
    
    # 3. Create a commit
    run_command(["git", "commit", "-m", "Automated force sync from local machine"], "Committing changes")

    # 4. Perform a force push (overwrites remote history)
    print("\n⚠️ WARNING: This will overwrite the state of the 'main' branch on GitHub.")
    print("This is the 'backup' you asked for.")
    confirmation = input("Do you want to continue with the force push? (yes/no): ")
    if confirmation.lower() == 'yes':
        run_command(["git", "push", "--force"], "Overwriting remote with local state")
        print("\n✨ Force sync complete. GitHub repository is now an exact copy of your local code.")
        print("You can now safely run 'pull_and_start.py' on your other machines.")
    else:
        print("\n❌ Push cancelled. No changes were made to the remote repository.")
        sys.exit(0)

if __name__ == "__main__":
    main()