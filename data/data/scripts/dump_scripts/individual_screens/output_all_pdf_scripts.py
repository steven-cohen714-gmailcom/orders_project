#!/usr/bin/env python3

import os
from pathlib import Path

# === CONFIGURATION ===
project_root = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = project_root / "scripts_for_each_screen" / "pdf_related_files.txt"

# Match content in files or filenames
content_keywords = {
    "weasyprint", "StreamingResponse", "write_pdf",
    "pdf_template", "showPDFModal", "application/pdf",
    "/preview_pdf_new_order", "/generate_pdf_for_order",
    "note_to_supplier", "logo_path", "order.total"
}
filename_keywords = {
    "pdf", "weasyprint"
}

# Always include these known paths
explicit_paths = {
    "backend/main.py",
    "frontend/static/js/new_order_main.js",
    "frontend/static/js/components/pdf_modal.js",
    "frontend/templates/pdf_template.html",
    "frontend/templates/new_order.html",
    "backend/endpoints/new_order_pdf_generator.py",
    "backend/endpoints/pending_order_pdf_generator.py"
}

matched_files = []

def is_pdf_related(file_path):
    rel = file_path.relative_to(project_root).as_posix()
    if rel in explicit_paths:
        return True

    name = file_path.name.lower()
    if any(k in name for k in filename_keywords):
        return True

    if file_path.suffix.lower() in {".py", ".js", ".html"}:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return any(k in f.read().lower() for k in content_keywords)
        except Exception:
            return False

    return False

# === SCAN FILES ===
for dirpath, _, files in os.walk(project_root):
    for file in files:
        full_path = Path(dirpath) / file
        if is_pdf_related(full_path):
            matched_files.append(full_path)

# === OUTPUT CONTENT ===
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as out:
    out.write("==== PDF-RELATED FILE CONTENTS ====\n\n")
    for path in sorted(matched_files):
        rel_path = path.relative_to(project_root)
        out.write(f"\n--- {rel_path} ---\n")
        try:
            with open(path, "r", encoding="utf-8") as f:
                out.write(f.read())
        except Exception as e:
            out.write(f"[Error reading file: {e}]\n")

print(f"✅ PDF-related file contents saved to:\n{output_file}")
