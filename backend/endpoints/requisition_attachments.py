# File: backend/endpoints/requisition_attachments.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path
from datetime import datetime
import shutil
import sqlite3

router = APIRouter(tags=["requisitions"])

DB_PATH = Path("data/orders.db")
UPLOADS_DIR = Path("data/uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Upload attachment using number (ID may be null) ---
@router.post("/upload_attachment")
async def upload_requisition_attachment(
    requisition_number: str = Form(...),
    file: UploadFile = File(...)
):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    stored_filename = f"{timestamp}_{file.filename}"
    stored_path = UPLOADS_DIR / stored_filename

    try:
        with stored_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        conn = get_db_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO requisition_attachments 
                (requisition_id, requisition_number, filename, file_path, upload_date)
                VALUES (NULL, ?, ?, ?, ?)
                """,
                (
                    requisition_number,
                    file.filename,
                    str(stored_path),
                    datetime.now().isoformat()
                )
            )

        return {"message": "Attachment uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# --- Get attachments by ID or Number ---
@router.get("/attachments/{identifier}")
def get_requisition_attachments(identifier: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Determine if ID or number
        if identifier.isdigit():
            cursor.execute(
                "SELECT filename, file_path FROM requisition_attachments WHERE requisition_id = ?",
                (int(identifier),)
            )
        else:
            cursor.execute(
                "SELECT filename, file_path FROM requisition_attachments WHERE requisition_number = ?",
                (identifier,)
            )

        results = cursor.fetchall()
        return {
            "attachments": [
                {"filename": row["filename"], "file_path": row["file_path"]}
                for row in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving attachments: {str(e)}")

@router.get("/uploads/{filename}")
def serve_uploaded_file(filename: str):
    file_path = UPLOADS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

# --- Submission models (unchanged) ---
class RequisitionItem(BaseModel):
    description: str
    quantity: int

class RequisitionPayload(BaseModel):
    requisitioner_id: int
    requisition_number: str
    requisition_date: str
    requisition_note: str
    items: List[RequisitionItem]

@router.post("/submit_requisition")
async def submit_requisition(data: RequisitionPayload, request: Request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO requisitions (
                requisitioner_id, requisition_number, requisition_date, requisition_note
            ) VALUES (?, ?, ?, ?)
        """, (
            data.requisitioner_id,
            data.requisition_number,
            data.requisition_date,
            data.requisition_note
        ))
        requisition_id = cursor.lastrowid

        for item in data.items:
            cursor.execute("""
                INSERT INTO requisition_items (requisition_id, description, quantity)
                VALUES (?, ?, ?)
            """, (requisition_id, item.description, item.quantity))

        # Relink orphaned attachments
        cursor.execute("""
            UPDATE requisition_attachments
            SET requisition_id = ?, requisition_number = NULL
            WHERE requisition_id IS NULL AND requisition_number = ?
        """, (requisition_id, data.requisition_number))

        conn.commit()
        return {"message": "Requisition submitted successfully", "id": requisition_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
