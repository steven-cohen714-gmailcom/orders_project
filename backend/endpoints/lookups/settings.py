from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

@router.get("/settings")
async def get_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT order_number_start, auth_threshold FROM settings WHERE id = 1")
        row = cursor.fetchone()
        if row:
            settings = {
                "order_number_start": row[0] if row[0] is not None else "URC1000",
                "auth_threshold": int(row[1]) if row[1] is not None else 0
            }
        else:
            settings = {"order_number_start": "URC1000", "auth_threshold": 0}
            cursor.execute("INSERT INTO settings (id, order_number_start, auth_threshold) VALUES (1, ?, ?)",
                          (settings["order_number_start"], settings["auth_threshold"]))
            conn.commit()
        logging.info(f"Settings fetched: {settings}")
        return settings
    except sqlite3.Error as e:
        logging.error(f"Database error fetching settings: {str(e)}")
        return {"order_number_start": "URC1000", "auth_threshold": 0}
    except Exception as e:
        logging.error(f"Error fetching settings: {str(e)}")
        return {"order_number_start": "URC1000", "auth_threshold": 0}
    finally:
        conn.close()

@router.put("/settings")
async def update_settings(request: dict):
    order_number_start = request.get("order_number_start")
    auth_threshold = request.get("auth_threshold")

    if not order_number_start or auth_threshold is None:
        logging.error("Missing order_number_start or auth_threshold in update settings request")
        raise HTTPException(status_code=400, detail="Missing order_number_start or auth_threshold")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET order_number_start = ?, auth_threshold = ? WHERE id = 1",
                      (order_number_start, auth_threshold))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO settings (id, order_number_start, auth_threshold) VALUES (1, ?, ?)",
                          (order_number_start, auth_threshold))
        conn.commit()
        logging.info(f"Settings updated: order_number_start = {order_number_start}, auth_threshold = {auth_threshold}")
        return {"message": "Settings updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")
    finally:
        conn.close()