from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")


@router.get("/suppliers")
async def get_suppliers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM suppliers")
        suppliers = cursor.fetchall()
        result = [{"id": s[0], "name": s[1]} for s in suppliers]
        logging.info(f"Suppliers fetched: {len(result)} items")
        return {"suppliers": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching suppliers: {str(e)}")
    finally:
        conn.close()


@router.post("/suppliers")
async def add_supplier(payload: dict):
    name = payload.get("name")
    if not name:
        logging.error("Missing name in add_supplier request")
        raise HTTPException(status_code=400, detail="Missing supplier name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO suppliers (name) VALUES (?)", (name,))
        conn.commit()
        logging.info(f"New supplier added: {name}")
        return {"message": "Supplier added successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error adding supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding supplier: {str(e)}")
    finally:
        conn.close()


@router.put("/suppliers/{supplier_id}")
async def update_supplier(supplier_id: int, payload: dict):
    new_name = payload.get("name")
    if not new_name:
        logging.error("Missing name in update_supplier request")
        raise HTTPException(status_code=400, detail="Missing supplier name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE suppliers SET name = ? WHERE id = ?", (new_name, supplier_id))
        if cursor.rowcount == 0:
            logging.warning(f"No supplier found with id {supplier_id}")
            raise HTTPException(status_code=404, detail="Supplier not found")
        conn.commit()
        logging.info(f"Supplier {supplier_id} updated to: {new_name}")
        return {"message": "Supplier updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating supplier: {str(e)}")
    finally:
        conn.close()