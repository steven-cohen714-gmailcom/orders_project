# backend/endpoints/lookups/users.py

from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")


@router.get("/users")
async def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, rights FROM users")
        users = cursor.fetchall()
        result = [{"id": u[0], "username": u[1], "rights": u[2]} for u in users]
        logging.info(f"Users fetched: {len(result)} items")
        return {"users": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    finally:
        conn.close()


@router.post("/users")
async def add_user(payload: dict):
    username = payload.get("username")
    password = payload.get("password")  # Stored raw for now (no hashing)
    rights = payload.get("rights")

    if not username or not password or not rights:
        logging.error("Missing username, password or rights in add_user request")
        raise HTTPException(status_code=400, detail="Missing username, password, or rights")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, rights) VALUES (?, ?, ?)",
            (username, password, rights)
        )
        conn.commit()
        logging.info(f"New user added: {username} with rights {rights}")
        return {"message": "User added successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error adding user: {str(e)}")
        raise HTTPException(status_code=400, detail="User could not be added (possibly duplicate username).")
    except sqlite3.Error as e:
        logging.error(f"Database error adding user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")
    finally:
        conn.close()


@router.put("/users/{user_id}")
async def update_user(user_id: int, payload: dict):
    new_username = payload.get("username")
    new_rights = payload.get("rights")

    if not new_username or not new_rights:
        logging.error("Missing username or rights in update_user request")
        raise HTTPException(status_code=400, detail="Missing username or rights")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, rights = ? WHERE id = ?",
            (new_username, new_rights, user_id)
        )
        if cursor.rowcount == 0:
            logging.warning(f"No user found with id {user_id} to update")
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        logging.info(f"User {user_id} updated: username -> {new_username}, rights -> {new_rights}")
        return {"message": "User updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")
    finally:
        conn.close()
