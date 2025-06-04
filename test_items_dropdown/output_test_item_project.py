from pathlib import Path

FILES = [
    "app.py",
    "orders.db",
    "test_item_dropdown.html",
    "test_item_dropdown.js",
    "test_item_fuzzy_dropdown.js",
]

output_lines = ["\n"]

for filename in FILES:
    output_lines.append("=" * 80)
    output_lines.append(f"📄 {filename}")
    output_lines.append("=" * 80)

    path = Path(__file__).parent / filename

    if not path.exists():
        output_lines.append("⚠️ File not found.")
        continue

    if path.suffix == ".db":
        output_lines.append("(Binary file - skipping full content)")
        continue

    try:
        content = path.read_text(encoding="utf-8")
        output_lines.append(content)
    except Exception as e:
        output_lines.append(f"⚠️ Error reading file: {e}")

    output_lines.append("")  # blank line between sections

# Write output to a file
output_path = Path(__file__).parent / "project_dump.txt"
output_path.write_text("\n".join(output_lines), encoding="utf-8")

# Also print to terminal
print("\n".join(output_lines))
