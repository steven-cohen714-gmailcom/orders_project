from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection

router = APIRouter()

# --- Schemas ---
class SettingsPayload(BaseModel):
    order_number_start: str
    auth_threshold_1: int
    auth_threshold_2: int
    auth_threshold_3: int
    auth_threshold_4: int

class OrderNumberPayload(BaseModel):
    order_number_start: str


# --- GET full settings ---
@router.get("/settings")
async def get_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4
        FROM settings WHERE id = 1
    """)
    row = cursor.fetchone()

    if row:
        settings = {
            "order_number_start": row["order_number_start"] or "URC1000",
            "auth_threshold_1": row["auth_threshold_1"] or 0,
            "auth_threshold_2": row["auth_threshold_2"] or 0,
            "auth_threshold_3": row["auth_threshold_3"] or 0,
            "auth_threshold_4": row["auth_threshold_4"] or 0
        }
    else:
        settings = {
            "order_number_start": "URC1000",
            "auth_threshold_1": 0,
            "auth_threshold_2": 0,
            "auth_threshold_3": 0,
            "auth_threshold_4": 0
        }
        cursor.execute("""
            INSERT INTO settings (id, order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4)
            VALUES (1, ?, ?, ?, ?, ?)
        """, (
            settings["order_number_start"],
            settings["auth_threshold_1"],
            settings["auth_threshold_2"],
            settings["auth_threshold_3"],
            settings["auth_threshold_4"]
        ))
        conn.commit()

    conn.close()
    return settings


# --- PUT full settings ---
@router.put("/settings")
async def update_settings(payload: SettingsPayload):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE settings
            SET order_number_start = ?, auth_threshold_1 = ?, auth_threshold_2 = ?, auth_threshold_3 = ?, auth_threshold_4 = ?
            WHERE id = 1
        """, (
            payload.order_number_start,
            payload.auth_threshold_1,
            payload.auth_threshold_2,
            payload.auth_threshold_3,
            payload.auth_threshold_4
        ))
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO settings (id, order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4)
                VALUES (1, ?, ?, ?, ?, ?)
            """, (
                payload.order_number_start,
                payload.auth_threshold_1,
                payload.auth_threshold_2,
                payload.auth_threshold_3,
                payload.auth_threshold_4
            ))
        conn.commit()
        return {"message": "Settings updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


# --- PUT order number only ---
@router.put("/order_number")
async def update_order_number(payload: OrderNumberPayload):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE settings SET order_number_start = ? WHERE id = 1
        """, (payload.order_number_start,))
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO settings (id, order_number_start)
                VALUES (1, ?)
            """, (payload.order_number_start,))
        conn.commit()
        return {"message": "Order number updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
