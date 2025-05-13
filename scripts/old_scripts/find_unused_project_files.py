#!/usr/bin/env python3

import os
import re

# Config
PROJECT_ROOT = "orders_project"
EXCLUDE_DIRS = {"venv", "__pycache__", ".git", ".idea", ".mypy_cache", ".pytest_cache"}
ALLOWED_EXTS = {".py", ".js", ".html"}

# Step 1: Collect all relevant file paths
file_paths = []
for root, dirs, files in os.walk(PROJECT_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in ALLOWED_EXTS:
            rel_path = os.path.relpath(os.path.join(root, f), PROJECT_ROOT)
            file_paths.append(rel_path)

# Step 2: Scan all files for references
references = set()
for root, dirs, files in os.walk(PROJECT_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext not in ALLOWED_EXTS:
            continue
        path = os.path.join(root, f)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                for target_path in file_paths:
                    base_name = os.path.splitext(target_path)[0]
                    if base_name in content:
                        references.add(target_path)
        except Exception as e:
            print(f"⚠️ Skipped unreadable file: {path}")

# Step 3: Report unused files
unused = sorted([fp for fp in file_paths if fp not in references])

if unused:
    print("\n📦 Possibly Unused Files:\n")
    for fp in unused:
        print(f"⚠️  {fp}")
    print(f"\n🔍 Total: {len(unused)} (verify manually before deleting!)")
else:
    print("✅ No unused files detected.")
