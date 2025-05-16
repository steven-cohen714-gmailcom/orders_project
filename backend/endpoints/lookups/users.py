from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import bcrypt

router = APIRouter()

@router.get("/users")  # Removed /lookups prefix
async def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, rights, auth_threshold_band FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": [{"id": u[0], "username": u[1], "rights": u[2], "auth_threshold_band": u[3]} for u in users]}

@router.post("/users")  # Removed /lookups prefix
async def add_user(username: str, password: str, rights: str, auth_threshold_band: int = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, rights, auth_threshold_band) VALUES (?, ?, ?, ?)",
            (username, password_hash, rights, auth_threshold_band)
        )
        conn.commit()
        return {"status": "User added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.put("/users/{user_id}")  # Removed /lookups prefix
async def update_user(user_id: int, username: str, password: str = None, rights: str = None, auth_threshold_band: int = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Fetch current user data
        cursor.execute("SELECT username, password_hash, rights, auth_threshold_band FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare updated values
        new_username = username or user[0]
        new_rights = rights or user[2]
        new_auth_threshold_band = auth_threshold_band if auth_threshold_band is not None else user[3]
        
        # Update password only if provided
        if password:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "UPDATE users SET username = ?, password_hash = ?, rights = ?, auth_threshold_band = ? WHERE id = ?",
                (new_username, password_hash, new_rights, new_auth_threshold_band, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET username = ?, rights = ?, auth_threshold_band = ? WHERE id = ?",
                (new_username, new_rights, new_auth_threshold_band, user_id)
            )
        
        conn.commit()
        return {"status": "User updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.delete("/users/{user_id}")  # Removed /lookups prefix
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