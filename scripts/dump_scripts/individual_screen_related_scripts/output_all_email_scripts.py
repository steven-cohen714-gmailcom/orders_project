from pathlib import Path
import os

# Set working directory
os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")

# Output file path
output_file = Path("scripts_for_each_screen/output_all_email_scripts.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

# Files specifically related to email functionality
email_files = [
    "frontend/static/js/send_email.js",
    "frontend/static/js/new_order_main.js",
    "backend/endpoints/order_email.py",
    "backend/utils/send_email.py",
    "backend/utils/emailer.py",
    "backend/main.py",
    ".env",
]

with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in email_files:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")
