from fastapi import HTTPException, Depends
from functools import wraps
from contextlib import contextmanager
import sqlite3
import logging
from typing import List, Dict, Any
from backend.database import get_db_connection

# Logging setup
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

# Database dependency
@contextmanager
def db_session():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

async def get_db():
    with db_session() as conn:
        yield conn

# Error handling decorator
def handle_db_errors(entity: str, action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except sqlite3.IntegrityError as e:
                logging.error(f"Integrity error {action} {entity}: {str(e)}")
                raise HTTPException(status_code=400, detail=f"{entity.capitalize()} could not be {action} (possible duplicate).")
            except sqlite3.Error as e:
                logging.error(f"Database error {action} {entity}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
            except Exception as e:
                logging.error(f"Error {action} {entity}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error {action} {entity}: {str(e)}")
        return wrapper
    return decorator

# Logging helpers
def log_success(entity: str, action: str, details: str):
    logging.info(f"{entity.capitalize()} {action}: {details}")

def log_warning(entity: str, message: str):
    logging.warning(f"{entity.capitalize()} {message}")

# Generic CRUD helpers
async def fetch_list(db: sqlite3.Connection, table: str, fields: List[str], response_key: str) -> Dict[str, List[Dict]]:
    cursor = db.cursor()
    cursor.execute(f"SELECT {', '.join(fields)} FROM {table}")
    rows = cursor.fetchall()
    result = [dict(zip(fields, row)) for row in rows]
    log_success(response_key, "fetched", f"{len(result)} items")
    return {response_key: result}

async def add_record(db: sqlite3.Connection, table: str, payload: Dict[str, Any], fields: List[str], log_message: str) -> Dict[str, str]:
    values = tuple(payload[field] for field in fields)
    placeholders = ", ".join(["?"] * len(fields))
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})", values)
    db.commit()
    log_success(table, "added", log_message)
    return {"message": f"{table.capitalize()} added successfully"}

async def update_record(db: sqlite3.Connection, table: str, record_id: int, payload: Dict[str, Any], fields: List[str], log_message: str) -> Dict[str, str]:
    values = tuple(payload[field] for field in fields) + (record_id,)
    set_clause = ", ".join(f"{field} = ?" for field in fields)
    cursor = db.cursor()
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE id = ?", values)
    if cursor.rowcount == 0:
        log_warning(table, f"No {table} found with id {record_id}")
        raise HTTPException(status_code=404, detail=f"{table.capitalize()} not found")
    db.commit()
    log_success(table, "updated", log_message)
    return {"message": f"{table.capitalize()} updated successfully"}