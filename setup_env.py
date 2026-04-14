#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).parent.resolve()
venv_dir = project_dir / "venv"

def run(command, desc):
    print(f"🔧 {desc}...")
    try:
        subprocess.run(command, check=True)
        print(f"✅ Done: {desc}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {desc}")
        sys.exit(1)

if not venv_dir.exists():
    run([sys.executable, "-m", "venv", "venv"], "Create virtual environment")

activate_script = venv_dir / "bin" / "activate"
if not activate_script.exists():
    print("❌ Virtual environment activation script not found")
    sys.exit(1)

pip_exec = venv_dir / "bin" / "pip"

run([pip_exec, "install", "--upgrade", "pip"], "Upgrade pip")
run([pip_exec, "install", "-r", str(project_dir / "requirements.txt")], "Install requirements")
