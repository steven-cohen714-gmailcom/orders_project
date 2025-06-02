from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.database import get_db_connection
import logging
import sqlite3
import csv

router = APIRouter()

# Configure logging
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@router.get("/suppliers")
async def get_suppliers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, account_number FROM suppliers")
        suppliers = cursor.fetchall()
        result = [{"id": s[0], "name": s[1], "account_number": s[2]} for s in suppliers]
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
    try:
        name = payload.get("name", "").strip()
        account_number = payload.get("account_number", "").strip()
        if not name:
            raise HTTPException(status_code=400, detail="Missing supplier name")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO suppliers (
                name, account_number, telephone, vat_number, registration_number,
                email, contact_name, contact_telephone,
                address_line1, address_line2, address_line3, postal_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            account_number,
            payload.get("telephone", ""),
            payload.get("vat_number", ""),
            payload.get("registration_number", ""),
            payload.get("email", ""),
            payload.get("contact_name", ""),
            payload.get("contact_telephone", ""),
            payload.get("address_line1", ""),
            payload.get("address_line2", ""),
            payload.get("address_line3", ""),
            payload.get("postal_code", "")
        ))

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
    name = payload.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Missing supplier name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE suppliers SET name = ? WHERE id = ?", (name, supplier_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Supplier not found")
        conn.commit()
        logging.info(f"Supplier {supplier_id} updated: {name}")
        return {"message": "Supplier updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating supplier: {str(e)}")
    finally:
        conn.close()

@router.post("/import_suppliers_csv")
async def import_suppliers_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        contents = await file.read()
        lines = contents.decode("utf-8").splitlines()
        reader = csv.DictReader(lines)

        suppliers = []
        for row in reader:
            account_number = row.get("code", "").strip()
            name = row.get("description", "").strip()
            if account_number and name:
                suppliers.append((name, account_number))

        if not suppliers:
            raise HTTPException(status_code=400, detail="CSV is empty or invalid.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers;")
        cursor.executemany(
            "INSERT INTO suppliers (name, account_number) VALUES (?, ?);",
            suppliers
        )
        conn.commit()
        conn.close()

        logging.info(f"✅ Imported {len(suppliers)} suppliers from CSV.")
        return {"inserted": len(suppliers)}
    except Exception as e:
        logging.error(f"❌ Error importing suppliers CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
