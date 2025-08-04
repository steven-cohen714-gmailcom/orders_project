import os
from pathlib import Path

# Configuration
LIVE_ROOT = Path("/home/steven_cohen714")
PROJECT_DIR = LIVE_ROOT / "orders_project"

# Items to keep (based on test machine root structure)
KEEP_ITEMS = {"orders_project"}

def clean_extra_files():
    """Remove files and directories not in KEEP_ITEMS, excluding data within orders_project."""
    print("🔄 Starting cleanup of extra files and directories...")
    for item in LIVE_ROOT.iterdir():
        item_name = item.name
        if item_name not in KEEP_ITEMS:
            if item.is_dir():
                print(f"🔄 Removing directory {item_name}...")
                os.system(f"rm -rf {item}")  # Use os.system for simplicity, no backup
                print(f"✅ Removed directory {item_name}.")
            else:
                print(f"🔄 Removing file {item_name}...")
                item.unlink(missing_ok=True)
                print(f"✅ Removed file {item_name}.")

def main():
    print("\n🚀 Starting live server cleanup to match test environment...")
    clean_extra_files()
    print("\n✨ Cleanup complete. Verify the root directory and test the application.")

if __name__ == "__main__":
    main()