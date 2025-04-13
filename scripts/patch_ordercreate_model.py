from pathlib import Path

target = Path("backend/endpoints/orders.py")
code = target.read_text()

patched = []
in_model = False

for line in code.splitlines():
    if line.strip().startswith("class OrderCreate("):
        in_model = True
    if in_model and "items:" in line:
        patched.append("    order_note: Optional[str] = None")
        patched.append("    supplier_note: Optional[str] = None")
        patched.append("    supplier_id: Optional[int] = None")
    patched.append(line)
    if in_model and line.strip().startswith("items:"):
        in_model = False

target.write_text("\n".join(patched))
print("✅ OrderCreate model patched with order_note, supplier_note, and supplier_id")
