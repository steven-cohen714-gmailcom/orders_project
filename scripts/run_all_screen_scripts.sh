#!/bin/bash

echo "▶️  Running all screen output scripts..."

SCRIPT_DIR="./output_scripts_to_txt_files/Individual_screens"

declare -a SCRIPTS=(
  "output_new_order_screen_files.py"
  "output_pending_orders_screen_files.py"
  "output_received_orders_screen_files.py"
  "output_audit_trail_screen_files.py"
  "output_home_screen_files.py"
  "output_login_screen_files.py"
  "output_maintenance_screen_files.py"
)

for script in "${SCRIPTS[@]}"; do
  echo "🔧 Running: $script"
  python "$SCRIPT_DIR/$script"
done

echo "✅ All .txt files regenerated in scripts_for_each_screen/"
