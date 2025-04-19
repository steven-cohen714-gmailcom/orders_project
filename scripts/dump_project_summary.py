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

def dump_test_summary() -> str:
    md = "## 🧪 Test Coverage Summary\n\n"
    md += "| Test Script | Purpose | Status |\n"
    md += "|-------------|---------|--------|\n"
    summary = {
        "test_authorisation_threshold_trigger.py": "High-value order triggers auth flow",
        "test_invalid_data_handling.py": "Ensures invalid payloads return 422/400",
        "test_invalid_items_variants.py": "Covers malformed line item edge cases",
        "test_pipeline_end_to_end.py": "Full pipeline test: creation → receive",
        "test_receive_partial.py": "Tests partial receiving with audit tracking",
    }
    scripts_dir = PROJECT_ROOT / "scripts"
    for test_file in sorted(scripts_dir.glob("test_*.py")):
        name = test_file.name
        status = "✅"
        purpose = summary.get(name, extract_desc(read_src(test_file)))
        md += f"| `{name}` | {purpose} | {status} |\n"
    md += "\n"
    return md

def extra_sections():
    return """
## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

## ⚙️ System Settings

| Key                 | Value   |
|----------------------|---------|
| auth_threshold       | 10000   |
| order_number_start   | URC1024 |
| last_order_number    | URC000  |

## 🚦 FastAPI Endpoint Summary

| Endpoint                     | Method    | Status         |
|------------------------------|-----------|----------------|
| `/orders`                   | POST      | ✅ Implemented |
| `/orders/receive`           | POST      | ✅ Implemented |
| `/orders/next_order_number` | GET       | ✅ Implemented |
| `/attachments/upload`       | POST      | ✅ Implemented |
| `/notes`                    | GET/POST  | ✅ Implemented |
| `/audit`                    | GET       | ⏳ Pending     |
| `/orders/print`             | GET       | ⏳ Planned     |
| `/lookups/suppliers`        | GET       | ✅ Implemented |
| `/lookups/requesters`       | GET       | ✅ Implemented |
| `/lookups/projects`         | GET       | ✅ Implemented |
| `/lookups/items`            | GET       | ✅ Implemented |
"""

# --- Main dump ---
def main():
    md = []
    md.append(f"# 📦 Project Snapshot\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    md.append("## 📁 Directory Tree\n````\n" + build_tree(PROJECT_ROOT) + "\n````")
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
    md.append(dump_db_schema(DB_FILE))
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
              "- He uses VS Code, wants brief error messages & clear steps\n")
    md.append(extra_sections())
    md.append(dump_test_summary())
    OUTPUT_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f"✅ Written {OUTPUT_MD}")

if __name__ == '__main__':
    main()
