# backend/endpoints/utils.py

from fastapi import APIRouter, HTTPException, Request
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Any
import json

router = APIRouter(tags=["utils"])

# --- Setup Log File ---
log_path = Path("logs/client.log")
log_path.parent.mkdir(exist_ok=True)

# File logger for structured client logs
logger = logging.getLogger("client")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(file_handler)


# --- Structured Log Endpoint ---
class ClientLog(BaseModel):
    level: str
    message: str
    details: Dict[str, Any]
    timestamp: str

@router.post("/log_client")
async def log_client(log: ClientLog) -> Dict[str, str]:
    """
    Log client-side messages to a server-side log file.

    Args:
        log: ClientLog object containing level, message, details, and timestamp.

    Returns:
        Dict with status message.

    Raises:
        HTTPException: If logging fails.
    """
    try:
        log_message = f"{log.message} | Details: {json.dumps(log.details)}"
        logger.log(
            getattr(logging, log.level.upper(), logging.INFO),
            log_message
        )
        return {"status": "Log recorded"}
    except Exception as e:
        logger.error(f"Failed to log client message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to log message: {str(e)}")


# --- Raw JS-Based Logging Endpoint (used by utils.js -> logToServer) ---
@router.post("/log")
async def log_from_frontend(request: Request):
    """
    Accept log submissions from frontend via utils.js and logToServer().
    """
    try:
        payload = await request.json()
        level = payload.get("level", "INFO").upper()
        message = payload.get("message", "")
        details = payload.get("details", {})

        log_entry = f"{level} | {message} | {json.dumps(details)}"

        if level == "ERROR":
            logger.error(log_entry)
        elif level == "WARNING":
            logger.warning(log_entry)
        else:
            logger.info(log_entry)

        return {"status": "ok"}
    except Exception as e:
        logger.exception("Failed to process /log call from frontend")
        raise HTTPException(status_code=500, detail=f"Failed to log message: {str(e)}")
