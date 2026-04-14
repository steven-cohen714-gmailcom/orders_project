# File: backend/endpoints/lookups/requisitioners.py

from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@router.get("/requisitioners")
async def get_requisitioners():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM requisitioners ORDER BY name")
        requisitioners = cursor.fetchall()
        # MODIFIED: Return a direct list of requisitioners instead of a dictionary with a "requisitioners" key.
        result = [{"id": r[0], "name": r[1]} for r in requisitioners]
        logging.info(f"Requisitioners fetched: {len(result)} items")
        return result
    except sqlite3.Error as e:
        logging.error(f"Database error fetching requisitioners: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching requisitioners: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching requisitioners: {str(e)}")
    finally:
        conn.close()

@router.post("/requisitioners")
async def add_requisitioner(payload: dict):
    name = payload.get("name")

    if not name:
        logging.error("Missing name in add_requisitioner request")
        raise HTTPException(status_code=400, detail="Missing requisitioner name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO requisitioners (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        new_id = cursor.lastrowid
        logging.info(f"New requisitioner added: {name}")
        return {
            "id": new_id,
            "name": name
        }
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error adding requisitioner: {str(e)}")
        raise HTTPException(status_code=400, detail="Requisitioner name might already exist.")
    except sqlite3.Error as e:
        logging.error(f"Database error adding requisitioner: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding requisitioner: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding requisitioner: {str(e)}")
    finally:
        conn.close()

@router.put("/requisitioners/{requisitioner_id}")
async def update_requisitioner(requisitioner_id: int, payload: dict):
    new_name = payload.get("name")

    if not new_name:
        logging.error("Missing name in update_requisitioner request")
        raise HTTPException(status_code=400, detail="Missing requisitioner name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE requisitioners SET name = ? WHERE id = ?",
            (new_name, requisitioner_id)
        )
        if cursor.rowcount == 0:
            logging.warning(f"No requisitioner found with id {requisitioner_id}")
            raise HTTPException(status_code=404, detail="Requisitioner not found")
        conn.commit()
        logging.info(f"Requisitioner {requisitioner_id} updated: name -> {new_name}")
        return {"message": "Requisitioner updated successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error updating requisitioner {requisitioner_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Requisitioner name might conflict with an existing requisitioner.")
    except sqlite3.Error as e:
        logging.error(f"Database error updating requisitioner {requisitioner_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating requisitioner {requisitioner_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating requisitioner: {str(e)}")
    finally:
        conn.close()

@router.delete("/requisitioners/{requisitioner_id}")
async def delete_requisitioner(requisitioner_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM requisitioners WHERE id = ?", (requisitioner_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Requisitioner not found")
        conn.commit()
        logging.info(f"Requisitioner {requisitioner_id} deleted successfully.")
        return {"message": "Requisitioner deleted successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error deleting requisitioner {requisitioner_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error deleting requisitioner {requisitioner_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting requisitioner: {str(e)}")
    finally:
        conn.close()