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
        result = [{"id": s[0], "name": s[1], "account_number": s[2] or ""} for s in suppliers]
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
        account_number = payload.get("account_number", "")
        name = payload.get("name", "")
        telephone = payload.get("telephone", "")
        vat_number = payload.get("vat_number", "")
        registration_number = payload.get("registration_number", "")
        email = payload.get("email", "")
        contact_name = payload.get("contact_name", "")
        contact_telephone = payload.get("contact_telephone", "")
        address_line1 = payload.get("address_line1", "")
        address_line2 = payload.get("address_line2", "")
        address_line3 = payload.get("address_line3", "")
        postal_code = payload.get("postal_code", "")

        if not name:
            raise HTTPException(status_code=400, detail="Missing supplier name")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO suppliers (
                account_number, name, telephone, vat_number, registration_number,
                email, contact_name, contact_telephone,
                address_line1, address_line2, address_line3, postal_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            account_number, name, telephone, vat_number, registration_number,
            email, contact_name, contact_telephone,
            address_line1, address_line2, address_line3, postal_code
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
    new_name = payload.get("name")
    new_account_number = payload.get("account_number", "")

    if not new_name:
        logging.error("Missing name in update_supplier request")
        raise HTTPException(status_code=400, detail="Missing supplier name")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE suppliers SET name = ?, account_number = ? WHERE id = ?",
            (new_name, new_account_number, supplier_id)
        )
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
            code = row.get("code", "").strip()
            description = row.get("description", "").strip()
            if code and description:
                suppliers.append((code, description))

        if not suppliers:
            raise HTTPException(status_code=400, detail="CSV is empty or invalid.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers;")
        cursor.executemany(
            "INSERT INTO suppliers (account_number, name) VALUES (?, ?);",
            suppliers
        )
        conn.commit()
        conn.close()

        logging.info(f"✅ Imported {len(suppliers)} suppliers from CSV.")
        return {"inserted": len(suppliers)}

    except Exception as e:
        logging.error(f"❌ Error importing suppliers CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@router.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Supplier not found")
        conn.commit()
        logging.info(f"Supplier {supplier_id} deleted")
        return {"message": "Supplier deleted successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error deleting supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error deleting supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting supplier: {str(e)}")
    finally:
        conn.close()
