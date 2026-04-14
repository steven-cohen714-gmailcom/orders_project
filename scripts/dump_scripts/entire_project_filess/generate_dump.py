# File: scripts/dump_scripts/entire_project_filess/generate_dump.py
# Purpose: Generate focused code dumps for a specific project area using presets.
# Behavior:
#   - Writes a timestamped dump file to ~/Desktop/orders_project_output_files/
#   - Fails loudly if any preset file is missing (prints absolute path)
#   - Optionally includes SQLite schema dump
#   - Includes project tree; defaults to depth=4 for 'evolution_export' if --tree not provided
# Notes:
#   - Project root is auto-detected by walking up until both 'backend' and 'frontend' dirs exist.

import os
import sys
import argparse
import subprocess
from pathlib import Path
import sqlite3
from datetime import datetime
from shutil import which

# --- File Utilities ---
def get_file_content(file_path: Path) -> str:
    """Reads file content, handling decoding errors."""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding="latin-1")
        except Exception as e:
            return f"[ERROR] Could not decode file: {e}\n"
    except Exception as e:
        return f"[ERROR] Could not read file: {e}\n"


def write_project_tree(outfile, project_root: Path, tree_depth: int) -> None:
    """Write a project tree to outfile, using system 'tree' if available, else Python fallback."""
    outfile.write("=" * 80 + "\n")
    outfile.write(f"PROJECT TREE (depth={tree_depth})\n")
    outfile.write("=" * 80 + "\n")
    try:
        if which("tree"):
            tree_output = subprocess.run(
                ["tree", "-L", str(tree_depth)],
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
                cwd=project_root
            )
            outfile.write(tree_output.stdout)
        else:
            # Python fallback when 'tree' is not installed
            def py_tree(root: Path, max_depth: int) -> str:
                lines = []
                root = Path(root).resolve()
                root_parts = len(root.parts)

                for current, dirs, files in os.walk(root):
                    cur_path = Path(current).resolve()
                    rel_parts = len(cur_path.parts) - root_parts
                    if rel_parts > max_depth:
                        dirs[:] = []
                        continue

                    indent = "  " * rel_parts
                    lines.append(f"{root.name}/" if rel_parts == 0 else f"{indent}{cur_path.name}/")

                    for f in sorted(files):
                        lines.append(f"{indent}  {f}")

                    if rel_parts >= max_depth:
                        dirs[:] = []
                return "\n".join(lines)

            outfile.write("[INFO] Using Python fallback; 'tree' command not found.\n")
            outfile.write(py_tree(project_root, tree_depth))
    except subprocess.TimeoutExpired:
        outfile.write("[ERROR] 'tree' command timed out.\n")
    except subprocess.CalledProcessError as e:
        outfile.write(f"[ERROR] 'tree' command failed: {e}\n")
    except Exception as e:
        outfile.write(f"[ERROR] Could not generate project tree: {e}\n")

    outfile.write("\n[END OF SECTION]\n\n")


# --- Main Logic ---
def main(args):
    # Determine the project root dynamically (walk up until both backend/ and frontend/ exist)
    script_path = Path(__file__).resolve()
    project_root = script_path.parent
    while not ((project_root / "backend").is_dir() and (project_root / "frontend").is_dir()):
        if project_root.parent == project_root:
            print("Error: Could not determine project root. Please run this script from within your project directory.")
            sys.exit(1)
        project_root = project_root.parent

    # Define the output directory and filename
    output_dir = Path.home() / "Desktop" / "orders_project_output_files"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    output_file_name = f"{args.preset}_{timestamp}.txt"
    output_file_path = output_dir / output_file_name

    # --- Presets ---
    presets = {
        "core_context": [
            "backend/main.py",
            "backend/database.py",
            "backend/endpoints/html_routes.py",  # Grok's correction
            "backend/utils/permissions_utils.py",
            "backend/utils/db_utils.py",
            "backend/utils/order_utils.py",
            "backend/utils/send_email.py",
            "frontend/templates/_tab_nav.html",
            "frontend/static/css/style.css",
            "frontend/static/js/components/utils.js",
            "frontend/static/js/components/shared_filters.js",
            "backend/endpoints/auth.py",
            "requirements.txt"  # Grok's suggestion
        ],
        "audit_trail": [
            "frontend/templates/audit_trail.html",
            "frontend/static/js/audit_trail.js",
            "frontend/static/js/audit_trail_expand.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/attachment_modal.js",
            "frontend/static/js/components/order_note_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction from .py to .js
            "frontend/static/js/components/receive_modal.js",
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/utils.js",
            "frontend/static/css/style.css",
            "backend/endpoints/audit_trail_filters.py",
            "backend/endpoints/orders.py",
            "backend/endpoints/order_queries.py",
            "backend/main.py",
            "backend/database.py",
            "backend/utils/permissions_utils.py",
            "backend/endpoints/lookups/users.py",
        ],
        "maintenance_users": [
            "frontend/templates/maintenance.html",
            "frontend/templates/edit_user_modal.html",
            "frontend/static/js/maintenance.js",  # Grok's correction from maintenance_main.js
            "frontend/static/js/maintenance_screen/users.js",
            "frontend/static/css/style.css",
            "backend/endpoints/lookups/users.py",
            "backend/endpoints/auth.py",
            "backend/database.py",
            "backend/utils/permissions_utils.py",
        ],
        "reports": [
            # Backend
            "backend/endpoints/reports.py",
            "backend/endpoints/html_routes.py",
            "backend/utils/permissions_utils.py",
            "backend/database.py",

            # Frontend: pages
            "frontend/templates/reports.html",
            "frontend/templates/report_view.html",

            # Frontend: JS powering the report view
            "frontend/static/js/report_view.js",

            # Shared UI bits used by filters/table
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/utils.js",
            "frontend/static/css/style.css",

            # Nav (gated by user_screen_permissions)
            "frontend/templates/_tab_nav.html",
        ],

        "new_order": [
            "frontend/templates/new_order.html",
            "frontend/static/js/new_order_main.js",
            "frontend/static/js/new_order_screen/submit_utils.js",
            "frontend/static/js/new_order_screen/submit_draft_order_utils.js",
            "frontend/static/js/new_order_screen/pdf_utils.js",
            "frontend/static/css/fuzzy_dropdown_fix.css",
            "backend/endpoints/orders.py",
            "backend/endpoints/draft_orders.py",
            "backend/endpoints/new_order_pdf_generator.py",
            "backend/endpoints/pending_order_pdf_generator.py",
            "backend/endpoints/order_notes.py",
            "frontend/static/js/components/fuzzy_dropdown.js",
            "frontend/static/js/components/utils.js",
            "backend/endpoints/lookups/items.py",
            "backend/endpoints/lookups/projects.py",
            "backend/endpoints/lookups/suppliers.py",
            "backend/endpoints/lookups/requesters.py",
        ],
        "pending_orders": [
            "frontend/templates/pending_orders.html",
            "frontend/static/js/pending_orders.js",  # Grok's correction from pending_orders_main.js
            "backend/endpoints/order_queries.py",  # Grok's correction - order_queries handles this
            "backend/endpoints/order_receiving.py",
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/receive_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
        ],
        "received_orders": [
            "frontend/templates/received_orders.html",
            "frontend/static/js/received_orders.js",  # Grok's correction from received_orders_main.js
            "backend/endpoints/order_queries.py",  # Grok's correction
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/order_note_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
        ],
        "partially_received_orders": [
            "frontend/templates/partially_delivered.html",  # Grok's correction
            "frontend/static/js/partially_delivered.js",  # Grok's correction
            "backend/endpoints/order_queries.py",  # Grok's correction
            "backend/endpoints/order_receiving.py",
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/receive_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
        ],
        "review_orders": [
            "frontend/templates/review_orders.html",
            "frontend/static/js/review_orders.js",
            "backend/endpoints/review_orders.py",
            "backend/endpoints/order_queries.py",  # Grok's correction
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/order_note_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
        ],
        "cod_orders": [
            "frontend/templates/cod_orders.html",
            "frontend/static/js/cod_orders.js",
            "backend/endpoints/order_queries.py",  # Grok's correction
            "backend/endpoints/lookups/mark_cod_paid_api.py",  # Grok's correction
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/order_note_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
        ],
        "draft_orders": [
            "frontend/templates/draft_orders.html",
            "frontend/static/js/draft_orders_main.js",
            "backend/endpoints/draft_orders.py",
            "backend/endpoints/order_queries.py",  # Grok's correction
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/js/components/expand_line_items.js",
            "frontend/static/js/components/order_note_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
        ],
        "lookups": [
            "frontend/templates/maintenance.html",  # Grok's correction
            "frontend/static/js/maintenance.js",  # Grok's correction
            "frontend/static/js/maintenance_screen/users.js",  # Grok's correction
            "frontend/static/js/maintenance_screen/requesters.js",
            "frontend/static/js/maintenance_screen/items.js",
            "frontend/static/js/maintenance_screen/suppliers.js",
            "frontend/static/js/maintenance_screen/projects.js",
            "frontend/static/js/maintenance_screen/requisitioners.js",
            "frontend/static/js/maintenance_screen/settings.js",
            "frontend/static/js/maintenance_screen/business_details.js",
            "backend/endpoints/lookups/items.py",
            "backend/endpoints/lookups/projects.py",
            "backend/endpoints/lookups/suppliers.py",
            "backend/endpoints/lookups/requesters.py",
            "backend/endpoints/lookups/users.py",
            "backend/endpoints/lookups/requisitioners.py",
            "backend/endpoints/lookups/settings.py",
            "backend/endpoints/lookups/business_details.py",
        ],
        "email_functionality": [
            "backend/utils/send_email.py",  # Grok's correction
            "backend/endpoints/order_notes.py",
            "backend/endpoints/order_receiving.py",
            "frontend/templates/email/order_note_notification.html",
            "frontend/templates/email/order_received_notification.html",
            "frontend/templates/email/password_reset.html",
        ],
        "attachments_and_pdf": [
            "backend/endpoints/order_attachments.py",
            "backend/endpoints/new_order_pdf_generator.py",
            "backend/endpoints/pending_order_pdf_generator.py",
            "frontend/static/js/components/attachment_modal.js",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
            "backend/utils/pdf_generator.py",
        ],
        "authorisations": [
            "frontend/templates/authorisations_per_user.html",
            "frontend/static/js/authorisations_per_user.js",
            "backend/endpoints/authorisations_api.py",  # Grok's correction
            "backend/utils/permissions_utils.py",
            "backend/endpoints/review_orders.py",
            "backend/endpoints/html_routes.py",
            "frontend/static/js/components/pdf_modal.js",  # Grok's correction
            "frontend/static/css/style.css",
            "frontend/templates/mobile/mobile_authorisations.html",
            "frontend/static/mobile/css/mobile_authorisations.css",
            "frontend/static/js/mobile/js/authorisations_screen/mobile_main.js",
            "backend/endpoints/mobile/mobile_awaiting_authorisation.py",
            "backend/endpoints/mobile/mobile_auth.py",
            "backend/endpoints/auth.py",
        ],
        "evolution_export": [
            # Backend
            "backend/endpoints/evolution_export.py",
            "backend/main.py",
            "backend/database.py",
            "backend/utils/permissions_utils.py",
            "backend/endpoints/lookups/users.py",

            # Frontend
            "frontend/templates/exports_evolution.html",
            "frontend/templates/_tab_nav.html",
            "frontend/static/js/exports_evolution.js",
            "frontend/static/js/components/utils.js",
            "frontend/static/js/components/shared_filters.js",
            "frontend/static/css/style.css",
        ],
    }

    files_to_include = presets.get(args.preset)
    if not files_to_include:
        print(f"Error: Preset '{args.preset}' not found. Available presets: {list(presets.keys())}")
        sys.exit(1)

    missing_files = []
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        # Header
        outfile.write(f"=== CODE DUMP: {args.preset.upper()} ===\n")
        outfile.write(f"Generated on: {timestamp}\n")
        outfile.write(f"Project Root: {project_root}\n\n")

        # Files
        for rel_path in files_to_include:
            file_path = project_root / rel_path
            outfile.write(f"{'='*92}FILE: {rel_path}\n")
            outfile.write("-" * 80 + "\n")
            if file_path.exists():
                outfile.write(get_file_content(file_path))
            else:
                err = f"[ERROR] File not found: {rel_path} (abs: {file_path.resolve()})\n"
                outfile.write(err)
                missing_files.append(f"{rel_path} (abs: {file_path.resolve()})")
            outfile.write("\n[END OF FILE]\n\n")

        # If files were missing, either fail (default) or continue when --allow-missing is set
        if missing_files:
            msg = "[MISSING FILES]\n" + "\n".join(f"- {m}" for m in missing_files) + "\n\n"
            outfile.write(msg)
            if not args.allow_missing:
                print("Preset had missing files. Rerun with --allow-missing to generate a partial dump.")
                sys.exit(2)

        # Schema
        if args.schema:
            outfile.write("=" * 80 + "\n")
            outfile.write("DATABASE SCHEMA\n")
            outfile.write("=" * 80 + "\n")
            db_path = project_root / "data" / "orders.db"
            if db_path.exists():
                conn = None
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name;")
                    for table_name, ddl in cursor.fetchall():
                        outfile.write(f"\n--- Table: {table_name} ---\n")
                        outfile.write(f"{ddl};\n")
                        cursor.execute(f"PRAGMA table_info({table_name});")
                        for col in cursor.fetchall():
                            # col tuple: (cid, name, type, notnull, dflt_value, pk)
                            outfile.write(f"  {col[1]} ({col[2]})\n")
                        cursor.execute(f"PRAGMA index_list({table_name});")
                        indices = cursor.fetchall()
                        if indices:
                            outfile.write("  Indexes:\n")
                            for idx in indices:
                                # idx tuple: (seq, name, unique, origin, partial)
                                outfile.write(f"    - {idx[1]}\n")
                except Exception as e:
                    outfile.write(f"[ERROR] Could not read database schema: {e}\n")
                finally:
                    try:
                        if conn:
                            conn.close()
                    except Exception:
                        pass
            else:
                outfile.write(f"[WARNING] Database file not found at {db_path}\n")
            outfile.write("\n[END OF SECTION]\n\n")

        # Project tree (depth defaulting for evolution_export)
        tree_depth = args.tree if args.tree is not None else (4 if args.preset == "evolution_export" else None)
        if tree_depth:
            write_project_tree(outfile, project_root, tree_depth)

    print(f"Successfully generated dump file at: {output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a focused code dump for a specific project area.")
    parser.add_argument("--preset", required=True, help="Preset to use, e.g., 'core_context', 'audit_trail', 'evolution_export'.")
    parser.add_argument("--schema", action="store_true", help="Include the database schema dump.")
    parser.add_argument("--tree", type=int, help="Include a directory tree to the specified depth.")
    parser.add_argument("--allow-missing", action="store_true", help="Do not abort on missing preset items; log them and continue.")
    args = parser.parse_args()
    main(args)
