# backend/endpoints/lookups/business_details.py

from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from backend.utils.db_utils import handle_db_errors, log_success
from backend.database import get_db_connection

router = APIRouter()

@router.get("/business_details")
@handle_db_errors(entity="business_details", action="fetching")
async def get_business_details():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number 
        FROM business_details 
        WHERE id = 1
    """)
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Business details not found")

    result = {
        "company_name": row[0],
        "address_line1": row[1],
        "address_line2": row[2],
        "city": row[3],
        "province": row[4],
        "postal_code": row[5],
        "telephone": row[6],
        "vat_number": row[7],
    }

    log_success("business_details", "fetched", "Company info retrieved")
    return result
