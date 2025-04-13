from pathlib import Path

# Set the root of the project and output file
project_root = Path(__file__).resolve().parents[1]
output_path = project_root / "full_script_dump.txt"

# Define which file types to include
target_extensions = {".py", ".html", ".js", ".css", ".md"}

# Collect all content
lines = []
for file in project_root.rglob("*"):
    if (
        file.is_file()
        and file.suffix in target_extensions
        and "venv" not in file.parts
        and "__pycache__" not in file.parts
    ):
        try:
            content = file.read_text(encoding="utf-8").strip()
            rel_path = file.relative_to(project_root)
            lines.append(f"{'='*80}\nFILE: {rel_path}\n{'='*80}\n{content}\n")
        except Exception as e:
            lines.append(f"{'='*80}\nFILE: {rel_path}\nERROR READING FILE: {e}\n")

# Write to a single markdown/text file
output_path.write_text("\n\n".join(lines), encoding="utf-8")
print(f"✅ Done. Contents written to: {output_path}")
