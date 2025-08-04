# backend/utils/db_utils.py

from fastapi import HTTPException
import functools
import logging
import sqlite3

LOG_PATH = "logs/server.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_success(entity: str, action: str, msg: str):
    logging.info(f"✅ [{entity.upper()}] Success {action}: {msg}")

def log_warning(entity: str, msg: str):
    logging.warning(f"⚠️ [{entity.upper()}] Warning: {msg}")

def log_error(entity: str, action: str, err: Exception):
    logging.error(f"❌ [{entity.upper()}] Failed {action}: {str(err)}")

def handle_db_errors(entity: str, action: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except sqlite3.DatabaseError as db_err:
                log_error(entity, action, db_err)
                raise HTTPException(status_code=500, detail="Database error occurred.")
            except Exception as e:
                log_error(entity, action, e)
                raise HTTPException(status_code=500, detail="Unexpected server error.")
        return wrapper
    return decorator
