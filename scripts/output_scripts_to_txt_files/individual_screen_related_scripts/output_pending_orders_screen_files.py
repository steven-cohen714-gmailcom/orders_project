from pathlib import Path
import os

os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_pending_orders_screen_files.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in [
        "frontend/templates/pending_orders.html",
        "frontend/static/js/pending_orders.js",
        "frontend/static/js/components/expand_line_items.js",
        "frontend/static/js/components/attachment_modal.js",
        "frontend/static/js/components/order_note_modal.js",
        "frontend/static/js/components/receive_modal.js",
        "frontend/static/js/components/shared_filters.js",
        "frontend/static/js/components/pdf_modal.js",
        "frontend/static/css/style.css",
        "backend/endpoints/orders.py",
        "backend/endpoints/order_attachments.py",
        "backend/endpoints/order_notes.py",
        "backend/endpoints/order_receiving.py",
        "backend/endpoints/order_pdf.py",
        "backend/endpoints/order_queries.py",
        "backend/endpoints/lookups.py",
        "backend/endpoints/html_routes.py",
        "backend/utils/order_utils.py",
        "backend/database.py",
        "backend/main.py",
    ]:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")
