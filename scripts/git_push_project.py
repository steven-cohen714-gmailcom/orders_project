import subprocess
import os
import sys
from pathlib import Path
import time

def run(command, desc, check=True, timeout=300, retries=3, delay=5):
    print(f"🔧 {desc}...")
    for attempt in range(retries):
        try:
            result = subprocess.run(command, check=check, capture_output=True, text=True, timeout=timeout)
            if result.stdout.strip() and "warning" not in result.stdout.lower():
                print(result.stdout.strip())
            return result
        except subprocess.TimeoutExpired:
            print(f"❌ {desc} timed out after {timeout} seconds (attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            elif check:
                print("❌ All retries timed out")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ {desc} failed (attempt {attempt + 1}/{retries})")
            print(e.stderr.strip())
            if attempt < retries - 1:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            elif check:
                print("❌ All retries failed")
                sys.exit(1)
            return e

def update_gitignore():
    gitignore = Path(".gitignore")
    entries = ["venv/", "*.pyc"]
    if gitignore.exists():
        with open(gitignore, 'r') as f:
            lines = f.read().splitlines()
        for entry in entries:
            if entry not in lines:
                lines.append(entry)
        with open(gitignore, 'w') as f:
            f.write("\n".join(lines) + "\n")
    else:
        with open(gitignore, 'w') as f:
            f.write("\n".join(entries) + "\n")
    run(["git", "add", ".gitignore"], "Stage .gitignore")

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📤 Git push process starting...")

    # Update .gitignore to exclude venv/ and .pyc files
    update_gitignore()

    # Stage specific files and directories
    paths_to_stage = [
        "backend/",
        "frontend/",
        "data/orders.db",
        "scripts/",
        "logs/",
    ]
    for path in paths_to_stage:
        if Path(path).exists():
            run(["git", "add", "--force", path], f"Stage {path}")

    # Commit changes
    result = run(["git", "commit", "-m", "Auto-commit by git_push_project.py"], "Commit changes", check=False)
    if "nothing to commit" in result.stderr.lower():
        print("✅ No changes to commit.")

    # Force push to origin/main
    run(["git", "push", "origin", "main", "--force"], "Force push to origin/main")

    print("✅ Git push completed successfully!")

if __name__ == "__main__":
    main()