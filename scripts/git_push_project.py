import subprocess
import os
import sys
from pathlib import Path

def run(command, desc, check=True):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        if result.stdout.strip() and "warning" not in result.stdout.lower():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr.strip())
        if check:
            sys.exit(1)
        return e

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📤 Git push process starting...")

    # Stage all changes, including data/orders.db
    run(["git", "add", ".", "--force"], "Stage all changes")

    # Commit changes
    result = run(["git", "commit", "-m", "Auto-commit by git_push_project.py"], "Commit changes", check=False)
    if "nothing to commit" in result.stderr.lower():
        print("✅ No changes to commit.")

    # Force push to origin/main
    run(["git", "push", "origin", "main", "--force"], "Force push to origin/main")

    print("✅ Git push completed successfully!")

if __name__ == "__main__":
    main()