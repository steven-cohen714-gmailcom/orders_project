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

    print("Starting git push for Universal Recycling Purchase Orders...")

    # Check for unstaged or staged changes
    status = run_git_command(["git", "status", "--porcelain"], "Failed to check git status")
    if status.strip():
        print("Changes detected, staging them...")
        run_git_command(["git", "add", "."], "Failed to stage changes")
        print("Committing changes...")
        run_git_command(["git", "commit", "-m", "Auto-commit for push"], "Failed to commit changes")
        committed = True
    else:
        committed = False

    # Check for uncommitted changes in index
    staged = run_git_command(["git", "diff", "--staged", "--quiet"], "Failed to check staged changes")
    if not staged.strip() or committed:
        # Pull with rebase to sync with remote
        print("Pulling latest changes from origin main...")
        try:
            run_git_command(["git", "pull", "--rebase", "origin", "main"], "Failed to pull changes")
        except subprocess.CalledProcessError:
            print("Error: Pull failed, likely due to conflicts. Run 'git status' to check conflicts, resolve them, then 'git rebase --continue'.")
            exit(1)

        # Push changes
        print("Pushing changes to origin main...")
        run_git_command(["git", "push", "origin", "main"], "Failed to push changes")
    else:
        print("No changes to commit or push.")

    print("Push completed successfully!")

if __name__ == "__main__":
    main()
