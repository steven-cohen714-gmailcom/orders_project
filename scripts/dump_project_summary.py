#!/usr/bin/env python3
import os
import sqlite3
import re
from pathlib import Path
from datetime import datetime

# --- Config ---
EXCLUDE_DIRS = {'venv', '__pycache__', '.pytest_cache'}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_MD = PROJECT_ROOT / 'project_summary.md'
DB_FILE = PROJECT_ROOT / 'data' / 'orders.db'

# --- Helpers ---
def build_tree(path: Path, prefix='') -> str:
    """Return an ASCII tree of the project structure up to depth 3, skipping excluded directories."""
    def _build(path, prefix, level):
        if level > 3:
            return []
        lines = []
        entries = sorted(p for p in path.iterdir() if not p.name.startswith('.') and p.name not in EXCLUDE_DIRS)
        for idx, entry in enumerate(entries):
            connector = '└── ' if idx == len(entries) - 1 else '├── '
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = '    ' if idx == len(entries) - 1 else '│   '
                lines.extend(_build(entry, prefix + extension, level + 1))
        return lines
    return f"{path}\n" + '\n'.join(_build(path, prefix, level=1))

def extract_desc(src: str) -> str:
    """Pull first triple‑quoted docstring or line‑comment as description."""
    m = re.search(r'"""(.*?)"""', src, re.DOTALL)
    if not m:
        m = re.search(r"'''(.*?)'''", src, re.DOTALL)
    if m:
        first = m.group(1).strip().splitlines()[0]
        return first
    for line in src.splitlines():
        if line.strip().startswith('#'):
            return line.strip().lstrip('# ').strip()
    return '(No description)'

def read_src(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f"<!-- ERROR reading {path.name}: {e} -->"

def dump_db_schema(db_path: Path) -> str:
    """Return Markdown of the SQLite schema and a brief purpose header."""
    md = "## 🗄️ Database Schema (`data/orders.db`)\n\n"
    if not db_path.exists():
        return md + "_No DB found_\n\n"
    md += "_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._\n\n"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for (tbl,) in cur.fetchall():
        md += f"### Table `{tbl}`\n"
        cur.execute(f"PRAGMA table_info({tbl});")
        for cid, name, dtype, notnull, dflt, pk in cur.fetchall():
            md += f"- `{name}` ({dtype}), pk={bool(pk)}, notnull={bool(notnull)}, default={dflt}\n"
        md += "\n"
    conn.close()
    return md

# --- Main dump ---
def main():
    md = []
    # Header
    md.append(f"# 📦 Project Snapshot\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    # Tree
    md.append("## 📁 Directory Tree\n```\n" + build_tree(PROJECT_ROOT) + "\n```\n")
    # Source files
    md.append("## 📄 Source Files\n")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in sorted(files):
            p = Path(root) / f
            if p == OUTPUT_MD: 
                continue
            rel = p.relative_to(PROJECT_ROOT)
            src = read_src(p)
            desc = extract_desc(src)
            md.append(f"### `{rel}`\n**{desc}**\n```python\n{src}\n```\n")
    # DB schema
    md.append(dump_db_schema(DB_FILE))
    # Narrative
    md.append("## 📝 Project summary\n"
              "I am busy building a Purchase Order system for Universal Recycling.\n\n"
              "**Testing Methodology:**\n"
              "- Each feature is tested in isolation (Python scripts, curl, direct sqlite3 queries)\n"
              "- No feature gets built on top of another until the one before it passes\n"
              "- Audit trails, status transitions, and data integrity are tested at every step\n"
              "- Test records are inserted programmatically, not by hand\n"
              "- UI will only be added when backend is rock solid\n\n"
              "**File Structure Summary:**\n"
              "- `backend/endpoints/orders.py` → Handles all `/orders` routes\n"
              "- `backend/database.py` → DB operations: init, insert, queries\n"
              "- `backend/utils/order_utils.py` → Helpers: status logic, validation\n"
              "- `scripts/` → Injection scripts, test runners & setup tools\n"
              "- `frontend/templates/` → Screen layouts (planned)\n"
              "- `data/orders.db` → Active SQLite file\n\n"
              "**Build Methodology:**\n"
              "- Build backend first → fully tested\n"
              "- One feature at a time → injected via `.py` scripts\n"
              "- No UI work until backend is rock solid\n"
              "- All tests confirmed via curl + Python\n"
              "- Full end-to-end integration test exists\n"
              "- Code reusability is a must (e.g. date handling, filters)\n\n"
              "**How Steven works with ChatGPT:**\n"
              "- Steven doesn’t know coding; he’s decent with terminal commands\n"
              "- He uses VS Code, wants brief error messages & clear steps\n")
    # Write out
    OUTPUT_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f"✅ Written {OUTPUT_MD}")

if __name__ == '__main__':
    main()

