from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from pathlib import Path

router = APIRouter(prefix="/lookups", tags=["requisitioners"])

DB_PATH = Path("data/orders.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------- Models ------------------- #

class Requisitioner(BaseModel):
    id: int
    name: str

class NewRequisitioner(BaseModel):
    name: str

# ------------------- Endpoints ------------------- #

@router.get("/requisitioners", response_model=List[Requisitioner])
async def get_requisitioners():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requisitioners ORDER BY name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching requisitioners: {str(e)}")

@router.post("/requisitioners", response_model=dict)
async def add_requisitioner(payload: NewRequisitioner):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requisitioners (name) VALUES (?)", (payload.name,))
            conn.commit()
            return {"status": "success", "id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Requisitioner already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding requisitioner: {str(e)}")

@router.delete("/requisitioners/{id}", response_model=dict)
async def delete_requisitioner(id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM requisitioners WHERE id = ?", (id,))
            conn.commit()
            return {"status": "deleted", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting requisitioner: {str(e)}")
