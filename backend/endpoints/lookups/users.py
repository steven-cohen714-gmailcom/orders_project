from fastapi import APIRouter, HTTPException, Request # Import Request
from pydantic import BaseModel, constr
from typing import Optional, List
from backend.database import get_db_connection
import bcrypt
import json
import sqlite3

router = APIRouter()

# ----------------------------
# Pydantic Models
# ----------------------------

class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=4)
    auth_threshold_band: Optional[int] = None

class UserUpdate(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: Optional[constr(strip_whitespace=True, min_length=4)] = None
    auth_threshold_band: Optional[int] = None
    screen_permissions: Optional[List[str]] = None # Frontend sends this list

# ----------------------------
# GET all users
# ----------------------------

@router.get("/users")
async def get_users():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, rights, auth_threshold_band FROM users")
    users_data = cursor.fetchall()
    
    result_users = []
    for u in users_data:
        user_id = u["id"]
        cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user_id,))
        screen_permissions = [row["screen_code"] for row in cursor.fetchall()]

        result_users.append({
            "id": u["id"],
            "username": u["username"],
            "rights": u["rights"],
            "auth_threshold_band": u["auth_threshold_band"],
            "roles": screen_permissions
        })
    conn.close()
    return {"users": result_users}

# ----------------------------
# POST: Add a new user
# ----------------------------

@router.post("/users")
async def add_user(payload: UserCreate):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, rights, auth_threshold_band) VALUES (?, ?, ?, ?)",
            (payload.username, password_hash, "edit", payload.auth_threshold_band)
        )
        conn.commit()
        return {"status": "User added successfully", "user_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# ----------------------------
# PUT: Update an existing user
# ----------------------------

@router.put("/users/{user_id}")
async def update_user(user_id: int, payload: UserUpdate, request: Request): # ADDED 'request: Request'
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        fields_to_update = {
            "username": payload.username,
            "rights": "edit",
            "auth_threshold_band": payload.auth_threshold_band
        }

        if payload.password and payload.password.strip():
            password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            fields_to_update["password_hash"] = password_hash
        
        set_clause = ", ".join([f"{key} = ?" for key in fields_to_update])
        values = list(fields_to_update.values()) + [user_id]

        cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)

        # --- Handle screen_permissions update using the screen_permissions table ---
        if payload.screen_permissions is not None:
            cursor.execute("DELETE FROM screen_permissions WHERE user_id = ?", (user_id,))
            
            for screen_code in payload.screen_permissions:
                cursor.execute(
                    "INSERT INTO screen_permissions (user_id, screen_code) VALUES (?, ?)",
                    (user_id, screen_code)
                )
        
        conn.commit()

        # --- NEW: Update the session if the current user's permissions were changed ---
        logged_in_user = request.session.get("user")
        if logged_in_user and logged_in_user["id"] == user_id:
            # Re-fetch the permissions directly from the DB to ensure they are current
            cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user_id,))
            updated_screen_permissions = [row["screen_code"] for row in cursor.fetchall()]
            request.session["screen_permissions"] = updated_screen_permissions
            print(f"Session permissions updated for user {user_id}: {updated_screen_permissions}") # Debugging line
        # --- END NEW ---

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
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("DELETE FROM screen_permissions WHERE user_id = ?", (user_id,))

        conn.commit()
        return {"status": "User deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
