from pathlib import Path

# Path to the orders.py file
f = Path("backend/endpoints/orders.py")

# Read the file content
text = f.read_text()

# Replace escaped triple quotes with proper triple quotes
fixed = text.replace('\"\"\"', '"""')

# Write the fixed content back to the file
f.write_text(fixed)

# Notify the user
print("✅ Fixed escaped triple quotes in orders.py")
