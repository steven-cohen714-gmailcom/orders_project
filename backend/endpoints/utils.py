from fastapi import APIRouter, HTTPException
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Any
import json

router = APIRouter(tags=["utils"])

# Ensure log directory exists
log_path = Path("logs/client.log")
log_path.parent.mkdir(exist_ok=True)
# Setup logging to client.log with file handler
logger = logging.getLogger('client')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_path)
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(handler)

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