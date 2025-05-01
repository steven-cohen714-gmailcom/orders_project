import subprocess
from pathlib import Path

# Absolute path to your Individual_screens directory
scripts_dir = Path(__file__).parent / "output_scripts_to_txt_files" / "individual_screens"

script_files = [
    "output_audit_trail_screen_files.py",
    "output_home_screen_files.py",
    "output_login_screen_files.py",
    "output_maintenance_screen_files.py",
    "output_new_order_screen_files.py",
    "output_pending_orders_screen_files.py",
    "output_received_orders_screen_files.py",
]

output_dir = Path(__file__).parent / "screen_outputs"
output_dir.mkdir(exist_ok=True)

for script_file in script_files:
    script_path = scripts_dir / script_file
    output_path = output_dir / script_file.replace(".py", ".txt")

    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        output_path.write_text(result.stdout)
        print(f"✅ Output written to {output_path.name}")
    except subprocess.CalledProcessError as e:
        error_msg = f"❌ Error running {script_file}:\n{e.stderr}"
        output_path.write_text(error_msg)
        print(error_msg)
