from pathlib import Path
import os

# Set working directory to project root
os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")

# Output file path
output_file = Path("scripts_for_each_screen/output_all_email_scripts.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

# Files related to email + PDF generation
email_related_files = [
    "frontend/static/js/send_email.js",
    "frontend/static/js/new_order_main.js",
    "backend/endpoints/order_email.py",
    "backend/endpoints/pdf_generator.py",
    "backend/utils/send_email.py",
    "backend/main.py",
    "frontend/templates/pdf_template.html",
    ".env",  # Only include if kept local — remove from shared exports
]

with open(output_file, "w", encoding="utf-8") as f:
    f.write("==== Universal Recycling: Email + PDF Script Bundle ====\n\n")

    for rel_path in email_related_files:
        f.write(f"📄 {rel_path}\n" + "-" * 60 + "\n")
        try:
            if rel_path == ".env":
                f.write("[INFO] .env file not shown for security. Remove this line if exporting privately.\n")
            else:
                with open(Path(rel_path), "r", encoding="utf-8") as src:
                    f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")
