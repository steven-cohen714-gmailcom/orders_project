from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

injected_code = '''
@router.post("")
async def create_new_order(order: OrderCreate):
    from ..database import create_order, get_setting, update_setting
    from ..utils.order_utils import generate_order_number, determine_status, validate_order_items
    import sqlite3
    from datetime import datetime

    try:
        validate_order_items(order.items)
        total = order.total

        auth_threshold = float(get_setting("auth_threshold"))
        current_order_number = get_setting("order_number_start")

        if not order.order_number:
            order.order_number = generate_order_number(current_order_number)
            next_order_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_order_number)

        status = determine_status(total, auth_threshold)

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO requesters (name) VALUES (?)", (order.requester,))
            conn.commit()

        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        return {"message": "Order created successfully", "order": result}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
'''

if __name__ == "__main__":
    text = TARGET.read_text()
    insert_index = text.rfind("@router.get")
    updated_code = text[:insert_index] + injected_code.strip() + "\n\n" + text[insert_index:]
    TARGET.write_text(updated_code)
    print("✅ Extended /orders route injected.")
