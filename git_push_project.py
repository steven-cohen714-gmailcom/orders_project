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
    project_dir = "/Users/stevencohen/Projects/universal_recycling/orders_project"
    if os.getcwd() != project_dir:
        try:
            os.chdir(project_dir)
        except FileNotFoundError:
            print(f"Error: Directory {project_dir} not found")
            exit(1)

    print("Starting git push for Universal Recycling Purchase Orders...")

    status = run_git_command(["git", "status", "--porcelain"], "Failed to check git status")
    stashed = False
    committed = False
    if status and status.strip():
        print("Changes detected, stashing them (including untracked files)...")
        run_git_command(["git", "stash", "push", "-u", "-m", "Auto-stash for push"], "Failed to stash changes")
        stashed = True

        print("Staging all changes...")
        run_git_command(["git", "add", "."], "Failed to stage changes")

        diff = run_git_command(["git", "diff", "--staged", "--quiet"], "Failed to check staged changes")
        if diff is None:
            print("Committing changes...")
            run_git_command(["git", "commit", "-m", "Auto-commit for push"], "Failed to commit changes")
            committed = True

    print("Pulling latest changes from origin main...")
    result = run_git_command(["git", "pull", "--rebase", "origin", "main"], "Failed to pull changes")
    if result is None:
        print("Error: Pull failed, likely due to conflicts.")
        print("Run 'git status' to check conflicts, resolve them, then 'git rebase --continue'.")
        if stashed:
            print("Restoring stashed changes...")
            run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
        exit(1)

    if committed or status.strip():
        print("Pushing changes to origin main...")
        result = run_git_command(["git", "push", "origin", "main"], "Failed to push changes")
        if result is None:
            print("Error: Push failed. Check network or run 'git status' for issues.")
            if stashed:
                print("Restoring stashed changes...")
                run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
            exit(1)
    else:
        print("No changes to commit or push.")

    if stashed:
        print("Restoring stashed changes...")
        result = run_git_command(["git", "stash", "pop"], "Failed to restore stashed changes")
        if result is None:
            print("Warning: Stash pop had conflicts. Run 'git stash show' and resolve manually.")

    print("Push completed successfully!")

if __name__ == "__main__":
    main()
