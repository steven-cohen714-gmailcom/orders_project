# File: backend/endpoints/orders/cod_orders_api.py

from fastapi import APIRouter, Request, HTTPException
from backend.database import get_db_connection

router = APIRouter()

@router.get("/orders/api/cod_orders")
def get_cod_orders():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.order_number, s.name AS supplier_name, o.created_date,
                       o.total, o.payment_terms, o.payment_date, o.amount_paid
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.id
                WHERE o.payment_terms = 'COD'
                ORDER BY o.created_date DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch COD orders: {str(e)}")
