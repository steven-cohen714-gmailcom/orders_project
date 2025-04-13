import subprocess
import os

def run_git_command(args, error_msg):
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_msg}")
        print(e.stderr)
        exit(1)

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

    # Check for unstaged changes
    status = run_git_command(["git", "status", "--porcelain"], "Failed to check git status")
    if status.strip():
        print("Unstaged changes detected, stashing them...")
        run_git_command(["git", "stash", "push", "-m", "Auto-stash for pull"], "Failed to stash changes")
        stashed = True
    else:
        stashed = False

    # Pull with rebase
    print("Pulling changes from origin main...")
    try:
        run_git_command(["git", "pull", "--rebase", "origin", "main"], "Failed to pull changes")
    except subprocess.CalledProcessError:
        print("Error: Pull failed, likely due to conflicts. Run 'git status' to check conflicts, resolve them, then 'git rebase --continue'.")
        if stashed:
            print("Restoring stashed changes...")
            run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
        exit(1)

    # Restore stashed changes if any
    if stashed:
        print("Restoring stashed changes...")
        run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")

    print("Pull completed successfully!")

if __name__ == "__main__":
    main()
