# File: backend/endpoints/lookups/settings.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db_connection

router = APIRouter()

# --- Schemas ---
class SettingsPayload(BaseModel):
    order_number_start: str
    requisition_number_start: str
    auth_threshold_1: int
    auth_threshold_2: int
    auth_threshold_3: int
    auth_threshold_4: int
    auth_threshold_5: int # This should be correctly recognized by Pydantic

class OrderNumberPayload(BaseModel):
    order_number_start: str

class RequisitionNumberPayload(BaseModel):
    requisition_number_start: str

# --- GET full settings ---
@router.get("/settings")
async def get_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    # This SELECT query is designed to fetch auth_threshold_5
    cursor.execute("""
        SELECT order_number_start, requisition_number_start,
               auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4, auth_threshold_5
        FROM settings WHERE id = 1
    """)
    row = cursor.fetchone()

    if row:
        settings = {
            "order_number_start": row["order_number_start"] or "URC1000",
            "requisition_number_start": row["requisition_number_start"] or "REQ1000",
            "auth_threshold_1": row["auth_threshold_1"] or 0,
            "auth_threshold_2": row["auth_threshold_2"] or 0,
            "auth_threshold_3": row["auth_threshold_3"] or 0,
            "auth_threshold_4": row["auth_threshold_4"] or 0,
            "auth_threshold_5": row["auth_threshold_5"] or 0 # This should be correctly included
        }
    else:
        # If no settings row exists, insert a default one including auth_threshold_5
        settings = {
            "order_number_start": "URC1000",
            "requisition_number_start": "REQ1000",
            "auth_threshold_1": 0,
            "auth_threshold_2": 0,
            "auth_threshold_3": 0,
            "auth_threshold_4": 0,
            "auth_threshold_5": 0 # Default value for auth_threshold_5 on initial insert
        }
        cursor.execute("""
            INSERT INTO settings (
                id, order_number_start, requisition_number_start,
                auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4, auth_threshold_5
            ) VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (
            settings["order_number_start"],
            settings["requisition_number_start"],
            settings["auth_threshold_1"],
            settings["auth_threshold_2"],
            settings["auth_threshold_3"],
            settings["auth_threshold_4"],
            settings["auth_threshold_5"]
        ))
        conn.commit()

    conn.close()
    return settings

# --- PUT full settings update ---
@router.put("/settings")
async def update_settings(payload: SettingsPayload):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # This UPDATE statement is designed to save auth_threshold_5
        cursor.execute("""
            UPDATE settings
            SET order_number_start = ?,
                requisition_number_start = ?,
                auth_threshold_1 = ?,
                auth_threshold_2 = ?,
                auth_threshold_3 = ?,
                auth_threshold_4 = ?,
                auth_threshold_5 = ? 
            WHERE id = 1
        """, (
            payload.order_number_start,
            payload.requisition_number_start,
            payload.auth_threshold_1,
            payload.auth_threshold_2,
            payload.auth_threshold_3,
            payload.auth_threshold_4,
            payload.auth_threshold_5 # This value should be passed correctly
        ))

        if cursor.rowcount == 0:
            # If no row was updated (i.e., it didn't exist), insert a new one
            cursor.execute("""
                INSERT INTO settings (
                    id, order_number_start, requisition_number_start,
                    auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4, auth_threshold_5
                ) VALUES (1, ?, ?, ?, ?, ?, ?, ?)
            """, (
                payload.order_number_start,
                payload.requisition_number_start,
                payload.auth_threshold_1,
                payload.auth_threshold_2,
                payload.auth_threshold_3,
                payload.auth_threshold_4,
                payload.auth_threshold_5
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
            UPDATE settings SET order_number_start = ?
            WHERE id = 1
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

# --- PUT requisition number only ---
@router.put("/requisition_number")
async def update_requisition_number(payload: RequisitionNumberPayload):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE settings SET requisition_number_start = ? WHERE id = 1
        """, (payload.requisition_number_start,))
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO settings (id, requisition_number_start)
                VALUES (1, ?)
            """, (payload.requisition_number_start,))
        conn.commit()
        return {"message": "Requisition number updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()