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
TODO_REGEX = re.compile(r"#\s*TODO[:\s]+(.+)", re.IGNORECASE)

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
    return f"📂 Root: {path}\n" + '\n'.join(_build(path, prefix, level=1))

def extract_desc(src: str) -> str:
    m = re.search(r'"""(.*?)"""', src, re.DOTALL) or re.search(r"'''(.*?)'''", src, re.DOTALL)
    if m:
        return m.group(1).strip().splitlines()[0]
    for line in src.splitlines():
        if line.strip().startswith('#'):
            return line.strip().lstrip('# ').strip()
    return '(No description)'

def read_src(path: Path) -> str:
    try:
        if path.suffix in {'.py', '.html', '.js', '.sh', '.md', '.txt'}:
            return path.read_text(encoding='utf-8')
        return ''
    except Exception as e:
        return f"<!-- ERROR reading {path.name}: {e} -->"

def group_files_by_type(files: list[Path]) -> dict:
    grouped = {'Python Files': [], 'HTML Templates': [], 'JS Scripts': [], 'Shell/Other': []}
    for f in files:
        if f.suffix == '.py':
            grouped['Python Files'].append(f)
        elif f.suffix == '.html':
            grouped['HTML Templates'].append(f)
        elif f.suffix == '.js':
            grouped['JS Scripts'].append(f)
        else:
            grouped['Shell/Other'].append(f)
    return grouped

def dump_source_files() -> str:
    all_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in sorted(files):
            p = Path(root) / f
            if p == OUTPUT_MD or p.name.startswith('.') or p.name == '.DS_Store':
                continue
            all_files.append(p)
    grouped = group_files_by_type(all_files)
    md = ""
    for group, files in grouped.items():
        md += f"## 📂 {group}\n\n"
        for p in sorted(files):
            rel = p.relative_to(PROJECT_ROOT)
            src = read_src(p)
            desc = extract_desc(src)
            if src.strip():
                md += f"### `{rel}`\n**{desc}**\n```python\n{src}\n```\n\n"
    return md

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
        purpose = summary.get(name, extract_desc(read_src(test_file)))
        status = "✅" if name in summary else "⏳"
        md += f"| `{name}` | {purpose} | {status} |\n"
    md += "\n"
    return md

def dump_static_todos() -> str:
    return """
## ✅ TODOs (Static Manual Items)

- [ ] Modularize long `.js` files into reusable components
- [ ] Finalize `/audit` route with filters + trail UI
- [ ] Finalize `/orders/print` layout + backend
- [ ] Add RBAC (role-based access control)
- [ ] Pagination on long tables (Pending/Received)
- [ ] Security audit on file uploads
- [ ] Normalize filenames and harden upload paths
- [ ] Add upload success/failure status to frontend
"""

def scan_for_code_todos() -> str:
    todos = []
    for root, _, files in os.walk(PROJECT_ROOT):
        for f in files:
            if f.endswith(('.py', '.js', '.html')):
                path = Path(root) / f
                try:
                    lines = path.read_text(encoding='utf-8').splitlines()
                    for i, line in enumerate(lines):
                        m = TODO_REGEX.search(line)
                        if m:
                            todos.append(f"- `{path.relative_to(PROJECT_ROOT)}`: {m.group(1).strip()}")
                except Exception:
                    continue
    if not todos:
        return "## ⛳ Auto-detected TODOs\n\n_None found._\n"
    return "## ⛳ Auto-detected TODOs\n\n" + '\n'.join(todos) + "\n"

def extra_sections() -> str:
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

# --- Main ---
def main():
    md = []
    md.append(f"# 📦 Project Snapshot\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    md.append("## 📁 Directory Tree\n````\n" + build_tree(PROJECT_ROOT) + "\n````")
    md.append(dump_source_files())
    md.append(dump_db_schema(DB_FILE))
    md.append(dump_static_todos())
    md.append(scan_for_code_todos())
    md.append("## 📝 Project summary\n"
              "This is a custom-built Purchase Order system for Universal Recycling.\n\n"
              "**Build & Testing Approach:**\n"
              "- Features are isolated and tested before being chained\n"
              "- Scripts inject DB rows or hit live endpoints for testing\n"
              "- Full `curl`, Python, and sqlite3 test coverage\n"
              "- UI is layered only on top of a tested backend\n")
    md.append(extra_sections())
    md.append(dump_test_summary())
    try:
        OUTPUT_MD.write_text('\n'.join(md), encoding='utf-8')
        print(f"✅ Written to: {OUTPUT_MD}")
    except Exception as e:
        print(f"❌ Failed to write MD file: {e}")

if __name__ == '__main__':
    main()
