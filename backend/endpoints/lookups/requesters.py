from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

@router.get("/requesters")
async def get_requesters():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM requesters ORDER BY id DESC")
        rows = cursor.fetchall()
        result = [{"id": row[0], "name": row[1]} for row in rows]
        logging.info(f"Requesters fetched: {len(result)} items")
        return {"requesters": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching requesters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching requesters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching requesters: {str(e)}")
    finally:
        conn.close()


@router.post("/requesters")
async def add_requester(payload: dict):
    name = payload.get("name")
    if not name:
        logging.error("Missing name in add_requester request")
        raise HTTPException(status_code=400, detail="Missing requester name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requesters (name) VALUES (?)", (name,))
        conn.commit()
        logging.info(f"New requester added: {name}")
        return {"message": "Requester added successfully", "id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Requester already exists.")
    except sqlite3.Error as e:
        logging.error(f"Database error adding requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding requester: {str(e)}")
    finally:
        conn.close()


@router.put("/requesters/{requester_id}")
async def update_requester(requester_id: int, payload: dict):
    new_name = payload.get("name")
    if not new_name:
        logging.error("Missing name in update_requester request")
        raise HTTPException(status_code=400, detail="Missing requester name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE requesters SET name = ? WHERE id = ?", (new_name, requester_id))
        if cursor.rowcount == 0:
            logging.warning(f"No requester found with id {requester_id}")
            raise HTTPException(status_code=404, detail="Requester not found")
        conn.commit()
        logging.info(f"Requester {requester_id} updated to: {new_name}")
        return {"message": "Requester updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating requester {requester_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating requester {requester_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating requester: {str(e)}")
    finally:
        conn.close()


@router.delete("/requesters/{requester_id}")
async def delete_requester(requester_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM requesters WHERE id = ?", (requester_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Requester not found")
        logging.info(f"Requester deleted: {requester_id}")
        return {"message": "Requester deleted", "id": requester_id}
    except sqlite3.Error as e:
        logging.error(f"Database error deleting requester {requester_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error deleting requester {requester_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting requester: {str(e)}")
    finally:
        conn.close()
