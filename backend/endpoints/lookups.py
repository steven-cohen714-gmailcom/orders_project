from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/lookups", tags=["lookup"])

@router.get("/suppliers")
def get_suppliers():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, account_number, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
        return {"suppliers": suppliers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load suppliers: {e}")
    
@router.get("/requesters")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
        return {"requesters": requesters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load requesters: {e}")


