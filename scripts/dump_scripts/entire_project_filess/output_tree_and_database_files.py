#!/usr/bin/env python3
# File: scripts/dump_scripts/tree_and_schema_dump.py

import os, subprocess, sqlite3
from datetime import datetime

ROOT = '/Users/stevencohen/Projects/universal_recycling/orders_project'
DB   = os.path.join(ROOT, 'data', 'orders.db')
OUT_DIR = '/Users/stevencohen/Desktop/project_output_files'
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
OUT = os.path.join(OUT_DIR, f'tree_and_schema_{ts}.txt')

os.makedirs(OUT_DIR, exist_ok=True)

def sep(f, title):
    f.write("\n" + "="*80 + "\n")
    f.write(f"--- {title} ---\n")
    f.write("="*80 + "\n")

def dump_tree(f):
    try:
        txt = subprocess.check_output(['tree', '-L', '4', ROOT], text=True)
        f.write(txt)
    except Exception as e:
        f.write(f"[tree error] {e}\n")

def dump_schema(f):
    if not os.path.exists(DB):
        f.write(f"[schema] DB not found: {DB}\n")
        return
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT sql FROM sqlite_master WHERE type IN ('table','index','trigger','view');")
        rows = cur.fetchall()
        conn.close()
        for (sql,) in rows:
            if sql:
                f.write(sql + "\n\n")
    except Exception as e:
        f.write(f"[schema error] {e}\n")

if __name__ == "__main__":
    with open(OUT, 'w', encoding='utf-8') as f:
        sep(f, "DIRECTORY TREE (L=4)")
        dump_tree(f)
        sep(f, "DATABASE SCHEMA (sqlite_master SQL)")
        dump_schema(f)
    print(f"Wrote: {OUT}")
