from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/requesters", tags=["requesters"])

@router.get("")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            result = [dict(row) for row in cursor.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
