from pathlib import Path
import sqlite3
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from starlette.requests import Request

TARGET = Path("../backend/endpoints/orders.py")

injected_code = """
from fastapi.responses import HTMLResponse
from starlette.requests import Request

@router.get("/orders/print/{order_id}", response_class=HTMLResponse)
def print_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute(\"\"\"
                SELECT order_number, status, created_date, received_date, total,
                       order_note, supplier_note, requester
                FROM orders
                WHERE id = ?
            \"\"\", (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            order_dict = {
                "order_number": order[0],
                "status": order[1],
                "created_date": order[2],
                "received_date": order[3],
                "total": order[4],
                "order_note": order[5],
                "supplier_note": order[6],
                "requester": order[7],
            }

            cursor.execute(\"\"\"
                SELECT item_code, item_description, project, qty_ordered, price, total
                FROM order_items
                WHERE order_id = ?
            \"\"\", (order_id,))
            order_items = cursor.fetchall()

        return templates.TemplateResponse("print_template.html", {
            "request": Request({}),
            "order": order_dict,
            "items": order_items
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating printable order: {str(e)}")
"""

if __name__ == "__main__":
    text = TARGET.read_text()
    insert_index = text.rfind("@router.get")
    updated_code = text[:insert_index] + injected_code.strip() + "\n\n" + text[insert_index:]
    TARGET.write_text(updated_code)
    print("✅ /orders/print/{order_id} route injected.")
