import os
import re

# Define root directory and what to exclude
PROJECT_ROOT = "orders_project"
EXCLUDE_DIRS = {"venv", "__pycache__", ".git", ".idea", ".mypy_cache", ".pytest_cache"}
ALLOWED_EXTS = {".py", ".js", ".html"}

# Collect all relevant files
file_paths = []
for root, dirs, files in os.walk(PROJECT_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in ALLOWED_EXTS:
            rel_path = os.path.relpath(os.path.join(root, f), PROJECT_ROOT)
            file_paths.append(rel_path)

# Build reference map from all files
references = set()
for root, dirs, files in os.walk(PROJECT_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        path = os.path.join(root, f)
        ext = os.path.splitext(f)[1]
        if ext not in ALLOWED_EXTS:
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                for fp in file_paths:
                    # Strip extensions for import-style references
                    base_name = os.path.splitext(fp)[0]
                    pattern = re.escape(base_name)
                    if re.search(rf'\b{pattern}\b', content):
                        references.add(fp)
        except Exception as e:
            print(f"Error reading {path}: {e}")

# Report unused files
print("\n📦 Unused Files Report:\n")
unused = 0
for fp in file_paths:
    if fp not in references:
        print(f"⚠️ Possibly unused: {fp}")
        unused += 1

if unused == 0:
    print("✅ All files appear to be in use.")
else:
    print(f"\n🔍 Total possibly unused: {unused}")
