# backend/endpoints/lookups/settings.py

from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")


@router.get("/settings")
async def get_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        rows = cursor.fetchall()
        settings = {row[0]: row[1] for row in rows} if rows else {}

        if "order_number_start" not in settings:
            settings["order_number_start"] = "URC1000"

        logging.info(f"Settings fetched: {settings}")
        return settings
    except sqlite3.Error as e:
        logging.error(f"Database error fetching settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching settings: {str(e)}")
    finally:
        conn.close()


@router.put("/settings")
async def update_settings(request: dict):
    key = request.get("key")
    value = request.get("value")

    if not key or value is None:
        logging.error("Missing key or value in update settings request")
        raise HTTPException(status_code=400, detail="Missing key or value")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        logging.info(f"Settings updated: {key} = {value}")
        return {"message": "Settings updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")
    finally:
        conn.close()
