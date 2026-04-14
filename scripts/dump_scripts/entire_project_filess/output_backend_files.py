#!/usr/bin/env python3
# File: scripts/dump_scripts/backend_dump.py

import os
from datetime import datetime

ROOT = '/Users/stevencohen/Projects/universal_recycling/orders_project'
BACK = os.path.join(ROOT, 'backend')
OUT_DIR = '/Users/stevencohen/Desktop/project_output_files'
VALID_EXT = {'.py', '.js', '.html'}
EXCLUDE_DIR_PARTS = {'venv', 'node_modules', 'logs', 'data', 'dump_scripts', '__pycache__'}

ts = datetime.now().strftime('%Y%m%d_%H%M%S')
OUT = os.path.join(OUT_DIR, f'backend_dump_{ts}.txt')
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
        out.write(f"BACKEND ROOT: {BACK}\n")
        if not os.path.isdir(BACK):
            out.write("[error] backend directory not found\n")
        else:
            for dp, _, fns in os.walk(BACK):
                if should_skip_dir(dp): 
                    continue
                for fn in sorted(fns):
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in VALID_EXT:
                        dump_file(out, os.path.join(dp, fn))
    print(f"Wrote: {OUT}")
