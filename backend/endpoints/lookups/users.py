from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from typing import Optional
from backend.database import get_db_connection
import bcrypt

router = APIRouter()

# ----------------------------
# Pydantic Models
# ----------------------------

class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=4)
    rights: str
    auth_threshold_band: Optional[int] = None

class UserUpdate(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: Optional[constr(strip_whitespace=True, min_length=4)] = None
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

        fields_to_update = {
            "username": payload.username,
            "rights": payload.rights,
            "auth_threshold_band": payload.auth_threshold_band
        }

        if payload.password and payload.password.strip():
            password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            fields_to_update["password_hash"] = password_hash

        set_clause = ", ".join([f"{key} = ?" for key in fields_to_update])
        values = list(fields_to_update.values()) + [user_id]

        cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
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
