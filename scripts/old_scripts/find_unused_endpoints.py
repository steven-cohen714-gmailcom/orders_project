import os
import re

# Folder with your endpoint files
endpoints_dir = "backend/endpoints"
extensions = ('.py',)
exclude_dirs = {'__pycache__', 'venv', '.git'}

# Collect all endpoint module names
endpoint_files = [
    f.replace('.py', '')
    for f in os.listdir(endpoints_dir)
    if f.endswith('.py') and not f.startswith('__')
]

# Add lookups subfolder modules
lookups_path = os.path.join(endpoints_dir, 'lookups')
if os.path.exists(lookups_path):
    endpoint_files += [f"lookups.{f.replace('.py','')}" for f in os.listdir(lookups_path) if f.endswith('.py')]

# Build regex patterns for each module
patterns = {name: re.compile(rf'\b(endpoints\.{name}|from endpoints\.{name}|import endpoints\.{name})\b') for name in endpoint_files}

# Search all project files (excluding venv, .git, etc.)
used = {name: False for name in endpoint_files}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as f:
                try:
                    content = f.read()
                    for name, pattern in patterns.items():
                        if pattern.search(content):
                            used[name] = True
                except Exception as e:
                    print(f"Error reading {path}: {e}")

# Print results
print("\n🔍 Endpoint Usage Check:\n")
for name, is_used in used.items():
    if is_used:
        print(f"✅ Used: endpoints.{name}")
    else:
        print(f"⚠️ Possibly Unused: endpoints.{name}")

