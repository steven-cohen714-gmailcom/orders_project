import subprocess
import os

def run_git_command(args, error_msg):
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_msg}")
        print(e.stderr)
        return None

def main():
    # Ensure we're in the project directory
    project_dir = "/Users/stevencohen/Projects/universal_recycling/orders_project"
    if os.getcwd() != project_dir:
        try:
            os.chdir(project_dir)
        except FileNotFoundError:
            print(f"Error: Directory {project_dir} not found")
            exit(1)

    print("Starting git pull for Universal Recycling Purchase Orders...")

    # Check for any changes (staged, unstaged, untracked)
    status = run_git_command(["git", "status", "--porcelain"], "Failed to check git status")
    stashed = False
    if status and status.strip():
        print("Changes detected, stashing them (including untracked files)...")
        run_git_command(["git", "stash", "push", "-u", "-m", "Auto-stash for pull"], "Failed to stash changes")
        stashed = True

    # Pull with rebase
    print("Pulling changes from origin main...")
    result = run_git_command(["git", "pull", "--rebase", "origin", "main"], "Failed to pull changes")
    if result is None:
        print("Error: Pull failed, likely due to conflicts.")
        print("Run 'git status' to check conflicts, resolve them, then 'git rebase --continue'.")
        if stashed:
            print("Restoring stashed changes...")
            result = run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
            if result is None:
                print("Warning: Stash pop had conflicts. Run 'git stash show' and resolve manually.")
        exit(1)

    # Restore stashed changes if any
    if stashed:
        print("Restoring stashed changes...")
        result = run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
        if result is None:
            print("Warning: Stash pop had conflicts. Run 'git stash show' and resolve manually.")

    print("Pull completed successfully!")

if __name__ == "__main__":
    main()
