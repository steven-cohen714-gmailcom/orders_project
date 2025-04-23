from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
output_md = project_root / "files_for_current_features.md"

file_specs = [
    ("backend/endpoints/orders.py", "FastAPI backend logic for creating, receiving, and listing orders."),
    ("backend/main.py", "Main FastAPI application setup and routing for the Pending Orders screen."),
    ("frontend/static/js/pending_orders.js", "JS logic for filtering, loading, and rendering pending orders."),
    ("frontend/templates/pending_orders.html", "HTML template for rendering the Pending Orders screen."),
    ("frontend/static/js/components/order_note_modal.js", "Reusable modal for editing and saving continuous order notes."),
    ("frontend/static/js/components/date_input.js", "Reusable date input formatter with smart formatting and navigation."),
    ("frontend/static/js/components/attachment_modal.js", "Handles file attachment upload and view logic for orders."),
    ("frontend/static/js/components/expand_line_items.js", "Displays expandable line items per order."),
    ("frontend/static/js/components/receive_modal.js", "Modal for marking orders or items as received."),
    ("frontend/static/js/components/shared_filters.js", "Loads and populates shared dropdown filters like suppliers/requesters."),
]

lines = []
for rel_path, description in file_specs:
    abs_path = project_root / rel_path
    lines.append(f"### `{rel_path}`\n**Purpose:** {description}\n")
    try:
        content = abs_path.read_text(encoding="utf-8")
        lines.append("```python\n" + content + "\n```\n")
    except Exception as e:
        lines.append(f"```text\n⚠️ Could not read file: {e}\n```\n")

output_md.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Dumped to: {output_md}")