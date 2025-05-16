from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection

router = APIRouter()

@router.get("/lookups/settings")
async def get_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4 FROM settings WHERE id = 1")
    row = cursor.fetchone()
    if row:
        settings = {
            "order_number_start": row[0] if row[0] is not None else "URC1000",
            "auth_threshold_1": int(row[1]) if row[1] is not None else 0,
            "auth_threshold_2": int(row[2]) if row[2] is not None else 0,
            "auth_threshold_3": int(row[3]) if row[3] is not None else 0,
            "auth_threshold_4": int(row[4]) if row[4] is not None else 0
        }
    else:
        settings = {
            "order_number_start": "URC1000",
            "auth_threshold_1": 0,
            "auth_threshold_2": 0,
            "auth_threshold_3": 0,
            "auth_threshold_4": 0
        }
        cursor.execute(
            "INSERT INTO settings (id, order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4) VALUES (1, ?, ?, ?, ?, ?)",
            (settings["order_number_start"], settings["auth_threshold_1"], settings["auth_threshold_2"], settings["auth_threshold_3"], settings["auth_threshold_4"])
        )
        conn.commit()
    conn.close()
    return settings

@router.put("/lookups/settings")
async def update_settings(order_number_start: str, auth_threshold_1: int, auth_threshold_2: int, auth_threshold_3: int, auth_threshold_4: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE settings SET order_number_start = ?, auth_threshold_1 = ?, auth_threshold_2 = ?, auth_threshold_3 = ?, auth_threshold_4 = ? WHERE id = 1",
            (order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4)
        )
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO settings (id, order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4) VALUES (1, ?, ?, ?, ?, ?)",
                (order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4)
            )
        conn.commit()
        return {"message": "Settings updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()