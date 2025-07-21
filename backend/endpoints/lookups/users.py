# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/lookups/users.py

from fastapi import APIRouter, HTTPException, Request
# Import ValidationError and ensure logging is available
from pydantic import BaseModel, constr, EmailStr, Field, ValidationError
from typing import Optional, List
from backend.database import get_db_connection
import bcrypt
import json
import sqlite3
import logging # Import logging for explicit error logging

router = APIRouter()

# ----------------------------
# Pydantic Models
# ----------------------------

class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=4)
    auth_threshold_band: Optional[int] = None
    email: Optional[EmailStr] = None 
    # Use Field with alias to robustly handle incoming data, ensuring default 0
    can_receive_payment_notifications: Optional[int] = Field(default=0, alias="can_receive_payment_notifications")


class UserUpdate(BaseModel):
    # For updates, fields are truly optional meaning if not provided in JSON, they won't be updated.
    # If provided as None/null, they will be explicitly set to None/NULL in DB.
    username: Optional[constr(strip_whitespace=True, min_length=1)] = None # Make username optional for update
    password: Optional[constr(strip_whitespace=True, min_length=4)] = None
    auth_threshold_band: Optional[int] = None
    screen_permissions: Optional[List[str]] = None
    email: Optional[EmailStr] = None 
    can_receive_payment_notifications: Optional[int] = None 

# ----------------------------
# GET all users
# ----------------------------

@router.get("/users")
async def get_users():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    # MODIFIED: Select new columns from users table
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
            "roles": screen_permissions, # Frontend expects 'roles' for screen_permissions
            "email": u["email"], 
            # Ensure 0 or 1 is returned for frontend consistency (DB might store NULL)
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
        raise HTTPException(status_code=409, detail="Username already exists.") # 409 Conflict

    password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        # Include new columns in INSERT statement
        cursor.execute(
            "INSERT INTO users (username, password_hash, rights, auth_threshold_band, email, can_receive_payment_notifications) VALUES (?, ?, ?, ?, ?, ?)",
            (payload.username, password_hash, "edit", payload.auth_threshold_band, payload.email, payload.can_receive_payment_notifications)
        )
        conn.commit()
        return {"status": "User added successfully", "user_id": cursor.lastrowid}
    # Catch Pydantic validation errors specifically to return their detail
    except ValidationError as ve: 
        logging.error(f"Pydantic validation error in add_user: {ve.errors()}") 
        conn.rollback()
        raise HTTPException(status_code=422, detail=ve.errors()) # Return validation errors as detail
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
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # --- CORRECTED: Select username along with ID ---
        cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        # --- END CORRECTED ---

        # Dynamically build the update statement based on fields present in the payload
        update_parts = []
        update_values = []

        # Pydantic's model_dump is useful here to get fields that were actually passed
        # exclude_unset=True means only fields explicitly provided in the request body are included.
        # This is crucial for partial updates.
        payload_dict = payload.model_dump(exclude_unset=True) 

        # Handle password hash separately
        password_to_hash = payload_dict.pop("password", None) # Remove 'password' from dict to process separately
        if password_to_hash and password_to_hash.strip():
            password_hash = bcrypt.hashpw(password_to_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_parts.append("password_hash = ?")
            update_values.append(password_hash)

        # Handle username uniqueness check if username is being updated
        if "username" in payload_dict:
            if payload_dict["username"] != existing_user["username"]: # Only check if username changed
                cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (payload_dict["username"], user_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=409, detail="Username already exists for another user.")

        # Handle screen_permissions separately
        screen_permissions_payload = payload_dict.pop("screen_permissions", None) # Remove from dict
        if screen_permissions_payload is not None: # Check if screen_permissions was explicitly provided in the payload
            # Delete existing permissions for this user
            cursor.execute("DELETE FROM screen_permissions WHERE user_id = ?", (user_id,))
            if screen_permissions_payload: # Only insert if the list of permissions is not empty
                for screen_code in screen_permissions_payload:
                    cursor.execute(
                        "INSERT INTO screen_permissions (user_id, screen_code) VALUES (?, ?)",
                        (user_id, screen_code)
                    )

        # Process remaining fields from payload_dict for SQL UPDATE
        for key, value in payload_dict.items():
            # For optional fields, if the value is explicitly None, set to NULL in DB
            if value is None:
                update_parts.append(f"{key} = NULL")
            else:
                update_parts.append(f"{key} = ?")
                update_values.append(value)
        
        if not update_parts: # If no fields to update (e.g., only password/permissions changed or empty payload)
            # This can happen if only screen_permissions or password were sent, as they are popped.
            # Or if no actual update fields were provided, just the ID/username in URL/path.
            conn.commit() # Commit any screen_permissions or username checks
            return {"status": "No main user fields to update, or fields already handled (e.g., password, screen permissions)."}
            
        set_clause = ", ".join(update_parts)
        values = update_values + [user_id]

        cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        
        conn.commit()

        # --- Update the session if the current user's permissions were changed ---
        logged_in_user = request.session.get("user")
        if logged_in_user and logged_in_user["id"] == user_id:
            # Re-fetch the user's full updated data
            cursor.execute("SELECT id, username, rights, auth_threshold_band, email, can_receive_payment_notifications FROM users WHERE id = ?", (user_id,))
            updated_user_data = cursor.fetchone()
            
            if updated_user_data:
                # Update session with new data
                request.session["user"] = {
                    "id": updated_user_data["id"],
                    "username": updated_user_data["username"],
                    "rights": updated_user_data["rights"],
                    "auth_threshold_band": updated_user_data["auth_threshold_band"],
                    "email": updated_user_data["email"], 
                    "can_receive_payment_notifications": 1 if updated_user_data["can_receive_payment_notifications"] else 0 
                }
                # Also re-fetch screen permissions as they might have changed
                cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user_id,))
                updated_screen_permissions = [row["screen_code"] for row in cursor.fetchall()]
                request.session["screen_permissions"] = updated_screen_permissions
                logging.info(f"Session permissions and user details updated for user {user_id}: {updated_screen_permissions}") 
        # --- END Update session ---

        return {"status": "User updated successfully"}

    # Catch Pydantic validation errors specifically to return their detail
    except ValidationError as ve: 
        logging.error(f"Pydantic validation error in update_user: {ve.errors()}") 
        conn.rollback()
        raise HTTPException(status_code=422, detail=ve.errors()) # Return validation errors as detail
    except HTTPException as he: # Catch custom HTTPExceptions (like 409 Conflict)
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