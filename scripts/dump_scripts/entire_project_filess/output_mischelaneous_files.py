#!/usr/bin/env python3
# File: scripts/dump_scripts/misc_dump.py

import os
from datetime import datetime

ROOT = '/Users/stevencohen/Projects/universal_recycling/orders_project'
OUT_DIR = '/Users/stevencohen/Desktop/project_output_files'
VALID_EXT = {'.py', '.js', '.html'}
EXCLUDE_DIR_PARTS = {'frontend', 'backend', 'venv', 'node_modules', 'logs', 'data', 'dump_scripts', '__pycache__'}

SPECIAL_FILES = [
    'requirements.txt',
    'requirements-dev.txt',
    'requirements_prod.txt',
    'database.py',
    'db.py',
]

ts = datetime.now().strftime('%Y%m%d_%H%M%S')
OUT = os.path.join(OUT_DIR, f'misc_dump_{ts}.txt')
os.makedirs(OUT_DIR, exist_ok=True)

def should_skip_dir(path):
    parts = set(path.split(os.sep))
    return bool(parts & EXCLUDE_DIR_PARTS)

def dump_file(fh, path):
    fh.write(f"\n--- FILE: {path} ---\n")
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as rf:
            fh.write(rf.read())
    except Exception as e:
        fh.write(f"[read error] {e}\n")
    fh.write(f"\n--- END FILE: {path} ---\n")

if __name__ == "__main__":
    with open(OUT, 'w', encoding='utf-8') as out:
        # 1) Dump special files if present at any depth
        for dp, _, fns in os.walk(ROOT):
            if 'dump_scripts' in dp:  # avoid recursing into ourselves
                continue
            for name in SPECIAL_FILES:
                if name in fns:
                    dump_file(out, os.path.join(dp, name))

        # 2) Dump any .py/.js/.html NOT under frontend/ or backend/
        for dp, _, fns in os.walk(ROOT):
            if should_skip_dir(dp): 
                continue
            for fn in sorted(fns):
                ext = os.path.splitext(fn)[1].lower()
                if ext in VALID_EXT:
                    dump_file(out, os.path.join(dp, fn))

    print(f"Wrote: {OUT}")
