from pathlib import Path
import os
import sqlite3
import subprocess

# Define the base directory of your project
# IMPORTANT: Ensure this path is correct for your environment.
# If you run this script from the project root, you might not need os.chdir.
# For example: project_root = Path(__file__).parent.parent
project_root = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")

# Change to the project root directory
try:
    os.chdir(project_root)
    print(f"Changed current directory to: {os.getcwd()}")
except FileNotFoundError:
    print(f"Error: Project root directory not found at {project_root}")
    exit(1)

# Define the output file path
output_dir = Path("scripts_for_each_screen")
output_file = output_dir / "output_maintenance_screen_files.txt"

# Ensure the output directory exists
try:
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Ensured output directory exists: {output_dir.resolve()}")
except Exception as e:
    print(f"Error creating output directory {output_dir}: {e}")
    exit(1)

print(f"Generating dump file: {output_file.resolve()}")

# List of relevant files to include in the dump
relevant_files = [
    "frontend/static/css/style.css",
    "backend/endpoints/html_routes.py",
    "backend/endpoints/lookups/settings.py",
    "backend/endpoints/lookups/users.py",
    "backend/endpoints/lookups/items.py",
    "backend/endpoints/lookups/suppliers.py",
    "backend/endpoints/lookups/projects.py",
    "backend/endpoints/lookups/requesters.py",
    "backend/endpoints/lookups/requisitioners.py",
    "backend/endpoints/utils.py",
    "backend/database.py",
    "backend/main.py",
    "frontend/templates/maintenance.html",
    "frontend/static/js/maintenance_screen/users.js",
    "frontend/static/js/maintenance_screen/requesters.js",
    "frontend/static/js/maintenance_screen/items.js",
    "frontend/static/js/maintenance_screen/suppliers.js",
    "frontend/static/js/maintenance_screen/projects.js",
    "frontend/static/js/maintenance_screen/settings.js",
    "frontend/static/js/maintenance_screen/business_details.js",
    "frontend/static/js/maintenance_screen/index.js",
    "frontend/static/js/maintenance.js",
    "frontend/templates/edit_user_modal.html",
]

with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in relevant_files:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        file_path = project_root / rel_path # Construct full path
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as src:
                content = src.read()
                f.write(content)
                if "" in content:
                    f.write("\n[⚠️ WARNING] Some characters could not be decoded and were replaced with .\n")
            print(f"  ✅ Added: {rel_path}")
        except FileNotFoundError:
            f.write(f"[ERROR] File not found: {file_path}\n")
            print(f"  ❌ ERROR: File not found: {rel_path}")
        except Exception as e:
            f.write(f"[ERROR] Could not read file {file_path}: {e}\n")
            print(f"  ❌ ERROR: Could not read file {rel_path}: {e}")
        f.write("\n\n")

    # --- Append DB Schema ---
    f.write("📦 DATABASE SCHEMA: data/orders.db\n" + "="*60 + "\n")
    db_path = project_root / "data/orders.db"
    try:
        if not db_path.exists():
            f.write(f"[ERROR] Database file not found: {db_path}\n")
            print(f"  ❌ ERROR: Database file not found: {db_path}")
        else:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for (table_name,) in tables:
                f.write(f"\n🔸 Table: {table_name}\n")
                cursor.execute(f"PRAGMA table_info({table_name});")
                for col in cursor.fetchall():
                    f.write(f"  {col[1]} ({col[2]})\n")
            conn.close()
            print("  ✅ Added: Database Schema")
    except Exception as e:
        f.write(f"[ERROR] Could not read database schema from {db_path}: {e}\n")
        print(f"  ❌ ERROR: Could not read database schema: {e}")
    f.write("\n\n")

    # --- Append Tree Output ---
    f.write("\n🌲 PROJECT TREE (depth=4)\n" + "="*60 + "\n")
    try:
        # Run 'tree' command from the project_root
        tree_output = subprocess.run(["tree", "-L", "4", project_root], capture_output=True, text=True, check=True)
        f.write(tree_output.stdout)
        print("  ✅ Added: Project Tree")
    except FileNotFoundError:
        f.write("[ERROR] 'tree' command not found. Please install it (e.g., 'brew install tree' on macOS, 'sudo apt-get install tree' on Debian/Ubuntu).\n")
        print("  ❌ ERROR: 'tree' command not found. Please install it.")
    except subprocess.CalledProcessError as e:
        f.write(f"[ERROR] 'tree' command failed with error: {e.stderr}\n")
        print(f"  ❌ ERROR: 'tree' command failed: {e.stderr}")
    except Exception as e:
        f.write(f"[ERROR] Could not generate project tree: {e}\n")
        print(f"  ❌ ERROR: Could not generate project tree: {e}")
    f.write("\n\n")

print(f"\nSuccessfully generated dump file at: {output_file.resolve()}")
print("Please upload this 'output_maintenance_screen_files.txt' file.")
