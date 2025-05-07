from pathlib import Path
import logging
import os
from datetime import datetime
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    filename="logs/script_execution.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# List of files to include for ALL ORDER SCREENS
FILES_TO_OUTPUT = [
    # HTML Templates
    "frontend/templates/pending_orders.html",
    "frontend/templates/received_orders.html",
    "frontend/templates/audit_trail.html",
    "frontend/templates/partially_delivered.html",

    # JS Main Scripts
    "frontend/static/js/pending_orders.js",
    "frontend/static/js/received_orders.js",
    "frontend/static/js/audit_trail.js",
    "frontend/static/js/partially_delivered.js",

    # Shared Components
    "frontend/static/js/components/expand_line_items.js",
    "frontend/static/js/components/attachment_modal.js",
    "frontend/static/js/components/order_note_modal.js",
    "frontend/static/js/components/pdf_modal.js",
    "frontend/static/js/components/receive_modal.js",
    "frontend/static/js/components/shared_filters.js",

    # Backend Endpoints
    "backend/endpoints/orders.py",
    "backend/endpoints/order_receiving.py",
    "backend/endpoints/order_queries.py",
    "backend/endpoints/order_pdf.py",
    "backend/endpoints/order_attachments.py",

    # Backend Routing & Database
    "backend/main.py",
    "backend/database.py"
]

@contextmanager
def change_dir(new_path):
    old_path = os.getcwd()
    os.chdir(new_path)
    try:
        yield
    finally:
        os.chdir(old_path)

def generate_output_file():
    project_root = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    output_file = project_root / "scripts_for_each_screen/output_all_order_screens.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    logging.info("Starting generation of output_all_order_screens.txt")

    with output_file.open('w', encoding='utf-8') as f:
        f.write(f"# Generated on {datetime.now().isoformat()}\n")
        f.write("# All files related to Pending / Received / Partial / Audit Order Screens\n\n")

        for rel_path in FILES_TO_OUTPUT:
            file_path = project_root / rel_path
            f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")

            if not file_path.exists():
                msg = f"[ERROR] File not found: {file_path}"
                f.write(msg + "\n\n")
                logging.error(msg)
                continue

            try:
                with file_path.open('r', encoding='utf-8') as src:
                    f.write(src.read() + "\n\n")
                    logging.info(f"Wrote contents of {rel_path}")
            except Exception as e:
                msg = f"[ERROR] Could not read file: {rel_path} - {e}"
                f.write(msg + "\n\n")
                logging.error(msg)

    logging.info("Finished generating output_all_order_screens.txt")

if __name__ == "__main__":
    with change_dir("/Users/stevencohen/Projects/universal_recycling/orders_project"):
        generate_output_file()
