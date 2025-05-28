from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.database import get_db_connection

router = APIRouter()

@router.get("/api/cod_orders")
def get_cod_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    supplier: Optional[int] = Query(None),
    requester: Optional[int] = Query(None),
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            query = """
                SELECT 
                    o.id, 
                    o.order_number, 
                    s.name AS supplier, 
                    o.created_date,
                    o.total, 
                    o.payment_terms, 
                    o.payment_date, 
                    o.amount_paid
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.id
                WHERE o.payment_terms = 'COD'
            """
            params = []

            if start_date and start_date != "All":
                query += " AND DATE(o.created_date) >= DATE(?)"
                params.append(start_date)

            if end_date and end_date != "All":
                query += " AND DATE(o.created_date) <= DATE(?)"
                params.append(end_date)

            if supplier and supplier != "All":
                query += " AND o.supplier_id = ?"
                params.append(supplier)

            if requester and requester != "All":
                query += " AND o.requester_id = ?"
                params.append(requester)

            query += " ORDER BY o.created_date DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return {"orders": [dict(row) for row in rows]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch COD orders: {str(e)}")
