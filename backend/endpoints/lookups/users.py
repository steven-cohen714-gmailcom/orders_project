# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/lookups/users.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, constr, EmailStr, Field, ValidationError, field_validator # ADDED field_validator
from typing import Optional, List
from backend.database import get_db_connection
import bcrypt
import json
import sqlite3
import logging 

router = APIRouter()

# ----------------------------
# Pydantic Models
# ----------------------------

class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=4)
    auth_threshold_band: Optional[int] = None 
    email: Optional[EmailStr] = None # Keep Optional[EmailStr]
    can_receive_payment_notifications: Optional[int] = Field(default=0, alias="can_receive_payment_notifications")

    @field_validator('email', mode='before') # ADD THIS VALIDATOR
    @classmethod
    def convert_empty_email_to_none(cls, v):
        if v == '':
            return None
        return v

class UserUpdate(BaseModel):
    username: Optional[constr(strip_whitespace=True, min_length=1)] = None 
    password: Optional[constr(strip_whitespace=True, min_length=4)] = None
    auth_threshold_band: Optional[int] = None
    screen_permissions: Optional[List[str]] = None
    email: Optional[EmailStr] = None # Keep Optional[EmailStr]
    can_receive_payment_notifications: Optional[int] = None 

    @field_validator('email', mode='before') # ADD THIS VALIDATOR
    @classmethod
    def convert_empty_email_to_none(cls, v):
        if v == '':
            return None
        return v

# ----------------------------
# GET all users
# ----------------------------

@router.get("/users")
async def get_users():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, rights, auth_threshold_band, email, can_receive_payment_notifications FROM users")
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
            "roles": screen_permissions, 
            "email": u["email"], 
            "can_receive_payment_notifications": 1 if u["can_receive_payment_notifications"] else 0 
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

    # Validate username uniqueness
    cursor.execute("SELECT id FROM users WHERE username = ?", (payload.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=409, detail="Username already exists.") 

    password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        # Assign default auth_threshold_band if not provided (from previous fix)
        default_auth_band = 1 
        auth_band_to_save = payload.auth_threshold_band if payload.auth_threshold_band is not None else default_auth_band

        # Include new columns in INSERT statement
        cursor.execute(
            "INSERT INTO users (username, password_hash, rights, auth_threshold_band, email, can_receive_payment_notifications) VALUES (?, ?, ?, ?, ?, ?)",
            (payload.username, password_hash, "edit", auth_band_to_save, payload.email, payload.can_receive_payment_notifications) 
        )
        conn.commit()
        return {"status": "User added successfully", "user_id": cursor.lastrowid}
    except ValidationError as ve: 
        logging.error(f"Pydantic validation error in add_user: {ve.errors()}") 
        conn.rollback()
        raise HTTPException(status_code=422, detail=ve.errors()) 
    except Exception as e:
        logging.error(f"Database or unexpected error in add_user: {e}", exc_info=True) 
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to add user: {str(e)}")
    finally:
        conn.close()

# ----------------------------
# PUT: Update an existing user
# ----------------------------

@router.put("/users/{user_id}")
async def update_user(user_id: int, payload: UserUpdate, request: Request):
    conn = get_db_connection(); # Ensure connection is made here
    conn.row_factory = sqlite3.Row; # Ensure row_factory is set
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_parts = []
        update_values = []

        payload_dict = payload.model_dump(exclude_unset=True) 

        password_to_hash = payload_dict.pop("password", None) 
        if password_to_hash and password_to_hash.strip():
            password_hash = bcrypt.hashpw(password_to_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_parts.append("password_hash = ?")
            update_values.append(password_hash)

        if "username" in payload_dict:
            if payload_dict["username"] != existing_user["username"]: 
                cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (payload_dict["username"], user_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=409, detail="Username already exists for another user.")

        screen_permissions_payload = payload_dict.pop("screen_permissions", None) 
        if screen_permissions_payload is not None: 
            cursor.execute("DELETE FROM screen_permissions WHERE user_id = ?", (user_id,))
            if screen_permissions_payload: 
                for screen_code in screen_permissions_payload:
                    cursor.execute(
                        "INSERT INTO screen_permissions (user_id, screen_code) VALUES (?, ?)",
                        (user_id, screen_code)
                    )

        for key, value in payload_dict.items():
            if value is None:
                update_parts.append(f"{key} = NULL")
            else:
                update_parts.append(f"{key} = ?")
                update_values.append(value)
        
        if not update_parts: 
            conn.commit() 
            return {"status": "No main user fields to update, or fields already handled (e.g., password, screen permissions)."}
            
        set_clause = ", ".join(update_parts)
        values = update_values + [user_id]

        cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        
        conn.commit()

        # --- Update the session if the current user's permissions were changed ---
        logged_in_user = request.session.get("user")
        if logged_in_user and logged_in_user["id"] == user_id:
            cursor.execute("SELECT id, username, rights, auth_threshold_band, email, can_receive_payment_notifications FROM users WHERE id = ?", (user_id,))
            updated_user_data = cursor.fetchone()
            
            if updated_user_data:
                request.session["user"] = {
                    "id": updated_user_data["id"],
                    "username": updated_user_data["username"],
                    "rights": updated_user_data["rights"],
                    "auth_threshold_band": updated_user_data["auth_threshold_band"],
                    "email": updated_user_data["email"], 
                    "can_receive_payment_notifications": 1 if updated_user_data["can_receive_payment_notifications"] else 0 
                }
                cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user_id,))
                updated_screen_permissions = [row["screen_code"] for row in cursor.fetchall()]
                request.session["screen_permissions"] = updated_screen_permissions
                logging.info(f"Session permissions and user details updated for user {user_id}: {updated_screen_permissions}") 
        # --- END Update session ---

        return {"status": "User updated successfully"}

    except ValidationError as ve: 
        logging.error(f"Pydantic validation error in update_user: {ve.errors()}") 
        conn.rollback()
        raise HTTPException(status_code=422, detail=ve.errors()) 
    except HTTPException as he: 
        conn.rollback()
        raise he
    except Exception as e:
        logging.error(f"Database or unexpected error in update_user: {e}", exc_info=True) 
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update user: {str(e)}")
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