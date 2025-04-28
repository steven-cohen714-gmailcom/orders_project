from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

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

@router.get("/requesters")
async def get_requesters():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM requesters")
        requesters = cursor.fetchall()
        result = [{"id": r[0], "name": r[1]} for r in requesters]
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

@router.get("/items")
async def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_code, item_description FROM items")
        items = cursor.fetchall()
        result = [{"item_code": i[0], "item_description": i[1]} for i in items]
        logging.info(f"Items fetched: {len(result)} items, response: {result}")
        return {"items": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")
    finally:
        conn.close()

@router.get("/projects")
async def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT project_code, project_name FROM projects")
        projects = cursor.fetchall()
        result = [{"project_code": p[0], "project_name": p[1]} for p in projects]
        logging.info(f"Projects fetched: {len(result)} items")
        return {"projects": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")
    finally:
        conn.close()

@router.get("/settings")
async def get_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings WHERE key = 'order_number_start'")
        setting = cursor.fetchone()
        if setting:
            result = {"order_number_start": setting[1]}
        else:
            result = {"order_number_start": "URC1000"}
        logging.info(f"Settings fetched: {result}")
        return result
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
    if not key or not value:
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

@router.get("/business_details")
async def get_business_details():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number FROM business_details LIMIT 1")
        details = cursor.fetchone()
        if not details:
            logging.warning("No business details found in database")
            raise HTTPException(status_code=404, detail="Business details not found")
        result = {
            "company_name": details[0],
            "address_line1": details[1],
            "address_line2": details[2],
            "city": details[3],
            "province": details[4],
            "postal_code": details[5],
            "telephone": details[6],
            "vat_number": details[7]
        }
        logging.info(f"Business details fetched: {result}")
        return result
    except sqlite3.Error as e:
        logging.error(f"Database error fetching business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching business details: {str(e)}")
    finally:
        conn.close()