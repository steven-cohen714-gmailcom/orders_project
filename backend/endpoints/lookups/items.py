# backend/endpoints/lookups/items.py

from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")


@router.get("/items")
async def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_code, item_description FROM items")
        items = cursor.fetchall()
        result = [{"item_code": i[1], "item_description": i[2]} for i in items]
        logging.info(f"Items fetched: {len(result)} items")
        return {"items": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")
    finally:
        conn.close()


@router.post("/items")
async def add_item(payload: dict):
    item_code = payload.get("item_code")
    item_description = payload.get("item_description")

    if not item_code or not item_description:
        logging.error("Missing item_code or item_description in add_item request")
        raise HTTPException(status_code=400, detail="Missing item code or description")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (item_code, item_description) VALUES (?, ?)",
            (item_code, item_description)
        )
        conn.commit()
        logging.info(f"New item added: {item_code} - {item_description}")
        return {"message": "Item added successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error adding item: {str(e)}")
        raise HTTPException(status_code=400, detail="Item code might already exist.")
    except sqlite3.Error as e:
        logging.error(f"Database error adding item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding item: {str(e)}")
    finally:
        conn.close()


@router.put("/items/{item_id}")
async def update_item(item_id: int, payload: dict):
    new_code = payload.get("item_code")
    new_description = payload.get("item_description")

    if not new_code or not new_description:
        logging.error("Missing item_code or item_description in update_item request")
        raise HTTPException(status_code=400, detail="Missing item code or description")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET item_code = ?, item_description = ? WHERE id = ?",
            (new_code, new_description, item_id)
        )
        if cursor.rowcount == 0:
            logging.warning(f"No item found with id {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
        conn.commit()
        logging.info(f"Item {item_id} updated: code -> {new_code}, description -> {new_description}")
        return {"message": "Item updated successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error updating item {item_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Item code might conflict with an existing item.")
    except sqlite3.Error as e:
        logging.error(f"Database error updating item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating item: {str(e)}")
    finally:
        conn.close()