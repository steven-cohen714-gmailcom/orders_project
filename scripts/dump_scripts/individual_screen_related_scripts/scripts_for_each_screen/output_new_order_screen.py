from pathlib import Path
import os

os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_new_order_screen_files.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in [
        "frontend/static/css/style.css",
        "backend/endpoints/html_routes.py",
        "backend/endpoints/lookups/settings.py",
        "backend/endpoints/lookups/users.py",
        "backend/endpoints/utils.py",
        "backend/database.py",
        "backend/main.py",
        "frontend/templates/new_order.html",
        "frontend/static/js/new_order_main.js",
        "frontend/static/js/new_order_modals.js",
        "frontend/static/js/components/pdf_modal.js",
        "backend/endpoints/new_order_pdf_generator.py",
    ]:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")
