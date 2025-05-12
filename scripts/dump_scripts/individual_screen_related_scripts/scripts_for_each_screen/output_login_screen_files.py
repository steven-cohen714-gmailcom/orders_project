from pathlib import Path
import os

os.chdir("/Users/stevencohen/Projects/universal_recycling/orders_project")
output_file = Path("scripts_for_each_screen/output_login_screen_files.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    for rel_path in [
        "frontend/templates/login.html",
        "frontend/static/js/login.js",
        "frontend/static/css/style.css",
        "backend/endpoints/auth.py",
        "backend/endpoints/html_routes.py",
        "backend/main.py",
    ]:
        f.write(f"📄 {rel_path}\n" + "-"*60 + "\n")
        try:
            with open(Path(rel_path), 'r', encoding='utf-8') as src:
                f.write(src.read())
        except Exception as e:
            f.write(f"[ERROR] Could not read file: {e}\n")
        f.write("\n\n")
