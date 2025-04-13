from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

new_route = """
@router.get("/next_order_number")
async def get_next_order_number():
    from ..database import get_setting
    current = get_setting("order_number_start")
    return {"next_order_number": current}
"""

if __name__ == "__main__":
    content = TARGET.read_text()
    inject_index = content.rfind("@router.get")
    updated = content[:inject_index] + new_route.strip() + "\n\n" + content[inject_index:]
    TARGET.write_text(updated)
    print("✅ /orders/next_order_number route injected.")
