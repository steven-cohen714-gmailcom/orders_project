#!/usr/bin/env python3
# File: scripts/dump_scripts/frontend_dump.py

import os
from datetime import datetime

ROOT = '/Users/stevencohen/Projects/universal_recycling/orders_project'
FRONT = os.path.join(ROOT, 'frontend')
OUT_DIR = '/Users/stevencohen/Desktop/project_output_files'
VALID_EXT = {'.py', '.js', '.html'}  # add '.css' if you want it
EXCLUDE_DIR_PARTS = {'venv', 'node_modules', 'logs', 'data', 'dump_scripts', '__pycache__'}

ts = datetime.now().strftime('%Y%m%d_%H%M%S')
OUT = os.path.join(OUT_DIR, f'frontend_dump_{ts}.txt')
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
        out.write(f"FRONTEND ROOT: {FRONT}\n")
        if not os.path.isdir(FRONT):
            out.write("[error] frontend directory not found\n")
        else:
            for dp, _, fns in os.walk(FRONT):
                if should_skip_dir(dp): 
                    continue
                for fn in sorted(fns):
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in VALID_EXT:
                        dump_file(out, os.path.join(dp, fn))
    print(f"Wrote: {OUT}")
