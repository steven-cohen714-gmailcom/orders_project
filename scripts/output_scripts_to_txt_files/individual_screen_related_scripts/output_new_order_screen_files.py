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

# List of files to include in the output
FILES_TO_OUTPUT = [
    "frontend/templates/new_order.html",
    "frontend/templates/login.html",
    "frontend/templates/home.html",
    "frontend/templates/_tab_nav.html",
    "frontend/static/js/new_order_main.js",
    "frontend/static/js/components/attachment_modal.js",
    "frontend/static/js/components/pdf_modal.js",
    "frontend/static/js/components/shared_filters.js",
    "frontend/static/js/new_order_modals.js",
    "frontend/static/js/login.js",
    "frontend/static/css/style.css",
    "backend/endpoints/orders.py",
    "backend/endpoints/order_attachments.py",
    "backend/endpoints/order_pdf.py",
    "backend/endpoints/html_routes.py",
    "backend/endpoints/auth.py",
    "backend/endpoints/pdf_generator.py",
    "backend/endpoints/lookups/requesters.py",
    "backend/endpoints/lookups/suppliers.py",
    "backend/endpoints/lookups/business_details.py"
    "backend/endpoints/lookups/items.py"
    "backend/endpoints/lookups/settings.py"
    "backend/endpoints/lookups/projects.py"
    "backend/endpoints/whatsapp.py",
    "backend/utils/order_utils.py",
    "backend/database.py",
    "backend/main.py",
    "backend/twilio/twilio_utils.py",
]

# Context manager for changing directory
@contextmanager
def change_dir(new_path):
    old_path = os.getcwd()
    os.chdir(new_path)
    try:
        yield
    finally:
        os.chdir(old_path)

# Main script
def generate_output_file():
    project_root = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    output_file = project_root / "scripts_for_each_screen/output_new_order_screen_files.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    logging.info("Starting generation of output_new_order_screen_files.txt")

    with output_file.open('w', encoding='utf-8') as f:
        # Write header
        f.write(f"# Generated on {datetime.now().isoformat()}\n")
        f.write("# Output of files related to the new order screen\n\n")

        for rel_path in FILES_TO_OUTPUT:
            file_path = project_root / rel_path
            f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
            logging.info(f"Processing file: {rel_path}")

            if not file_path.exists():
                error_msg = f"[ERROR] File not found: {file_path}"
                f.write(error_msg + "\n")
                logging.error(error_msg)
                continue

            try:
                with file_path.open('r', encoding='utf-8') as src:
                    f.write(src.read())
                    logging.info(f"Successfully wrote {rel_path}")
            except UnicodeDecodeError:
                error_msg = f"[ERROR] File is not a text file or has invalid encoding: {file_path}"
                f.write(error_msg + "\n")
                logging.error(error_msg)
            except PermissionError:
                error_msg = f"[ERROR] Permission denied reading file: {file_path}"
                f.write(error_msg + "\n")
                logging.error(error_msg)
            except Exception as e:
                error_msg = f"[ERROR] Could not read file: {file_path} - {str(e)}"
                f.write(error_msg + "\n")
                logging.error(error_msg)
            f.write("\n\n")

    logging.info("Completed generation of output_new_order_screen_files.txt")

if __name__ == "__main__":
    with change_dir("/Users/stevencohen/Projects/universal_recycling/orders_project"):
        generate_output_file()