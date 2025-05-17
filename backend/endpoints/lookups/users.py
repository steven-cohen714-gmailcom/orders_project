from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db_connection
import bcrypt

router = APIRouter()

# ----------------------------
# Pydantic Models
# ----------------------------

class UserCreate(BaseModel):
    username: str
    password: str
    rights: str
    auth_threshold_band: Optional[int] = None

class UserUpdate(BaseModel):
    username: str
    password: Optional[str] = None
    rights: str
    auth_threshold_band: Optional[int] = None

# ----------------------------
# GET all users
# ----------------------------

@router.get("/users")
async def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, rights, auth_threshold_band FROM users")
    users = cursor.fetchall()
    conn.close()
    return {
        "users": [
            {
                "id": u[0],
                "username": u[1],
                "rights": u[2],
                "auth_threshold_band": u[3]
            } for u in users
        ]
    }

# ----------------------------
# POST: Add a new user
# ----------------------------

@router.post("/users")
async def add_user(payload: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, rights, auth_threshold_band) VALUES (?, ?, ?, ?)",
            (payload.username, password_hash, payload.rights, payload.auth_threshold_band)
        )
        conn.commit()
        return {"status": "User added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# ----------------------------
# PUT: Update an existing user
# ----------------------------

@router.put("/users/{user_id}")
async def update_user(user_id: int, payload: UserUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        if payload.password:
            password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "UPDATE users SET username = ?, password_hash = ?, rights = ?, auth_threshold_band = ? WHERE id = ?",
                (payload.username, password_hash, payload.rights, payload.auth_threshold_band, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET username = ?, rights = ?, auth_threshold_band = ? WHERE id = ?",
                (payload.username, payload.rights, payload.auth_threshold_band, user_id)
            )

        conn.commit()
        return {"status": "User updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# ----------------------------
# DELETE: Remove a user
# ----------------------------

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        return {"status": "User deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
