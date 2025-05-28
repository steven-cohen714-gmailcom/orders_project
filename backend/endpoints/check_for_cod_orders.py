from fastapi import APIRouter
import sqlite3
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/orders/api/check_for_cod_orders")
def check_for_cod_orders():
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()

        # Adjust this condition as needed
        query = """
            SELECT id, order_number, created_date
            FROM orders
            WHERE note_to_supplier LIKE '%COD%'
              AND status IN ('pending', 'awaiting authorisation')
              AND datetime(created_date) >= datetime('now', '-1 minute')
            ORDER BY created_date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        orders = [{"id": r[0], "order_number": r[1], "created_date": r[2]} for r in rows]
        return {"new_cod_orders": orders}

    except Exception as e:
        return {"error": str(e)}
