#!/usr/bin/env python3

import os
from pathlib import Path

# --- Config ---
project_root = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = project_root / "text_files_for_ai" / "environmental_files.txt"

# Keywords/patterns to match
env_keywords = {
    ".env",
    ".gitignore",
    "requirements.txt",
    "Pipfile",
    "pyproject.toml",
    "auth.py",
    "admin.py",
    "html_routes.py",
    "main.py",
    "session",
    "login.html",
    "home.html",
    "index.html",
    "tab_nav.html",
    "print_template.html"
}

# Results
environmental_files = []

def is_environmental_file(file_path):
    filename = file_path.name.lower()
    return any(keyword in filename for keyword in env_keywords)

# Scan project
for dirpath, _, filenames in os.walk(project_root):
    for file in filenames:
        full_path = Path(dirpath) / file
        if is_environmental_file(full_path):
            relative = full_path.relative_to(project_root)
            environmental_files.append(str(relative))

# Write output
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("==== Indirect / Environmental Files in Project ====\n\n")
    for path in sorted(environmental_files):
        f.write(f"{path}\n")

print(f"✅ Environmental file list saved to:\n{output_file}")
