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
# Avoid duplicate handlers on reload
if not logger.handlers:
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(file_handler)
    logger.propagate = False


# --- Structured Log Endpoint ---
class ClientLog(BaseModel):
    level: str
    message: str
    details: Dict[str, Any] = {}
    timestamp: str

@router.post("/log_client")
async def log_client(log: ClientLog) -> Dict[str, str]:
    """Log client-side messages to a server-side log file."""
    try:
        level_no = getattr(logging, log.level.upper(), logging.INFO)
        log_message = f"{log.message} | Details: {json.dumps(log.details, default=str)}"
        logger.log(level_no, log_message)
        return {"status": "Log recorded"}
    except Exception as e:
        logger.error(f"Failed to log client message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to log message: {e}")


# --- Raw JS-Based Logging Endpoint (used by utils.js -> logToServer) ---
@router.post("/log")
async def log_from_frontend(request: Request) -> Dict[str, str]:
    """Accept log submissions from frontend via utils.js and logToServer()."""
    try:
        payload = await request.json()
        level = str(payload.get("level", "INFO")).upper()
        message = str(payload.get("message", ""))
        details = payload.get("details", {})

        log_entry = f"{level} | {message} | {json.dumps(details, default=str)}"

        if level == "ERROR":
            logger.error(log_entry)
        elif level in ("WARN", "WARNING"):
            logger.warning(log_entry)
        else:
            logger.info(log_entry)

        return {"status": "ok"}
    except Exception as e:
        logger.exception("Failed to process /log call from frontend")
        raise HTTPException(status_code=500, detail=f"Failed to log message: {e}")
    

# --- Whoami (non-mobile replacement for /mobile/get_user_info) ---
@router.get("/api/me")
async def whoami(request: Request) -> Dict[str, Any]:
    raw = request.session.get("user")
    try:
        return json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        return {}
