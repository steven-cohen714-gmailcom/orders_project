from fastapi import APIRouter, HTTPException
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(tags=["utils"])

# Setup logging to client.log
logging.basicConfig(
    filename="logs/client.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s | Details: %(details)s"
)

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
        logging.log(
            getattr(logging, log.level.upper(), logging.INFO),
            log.message,
            extra={"details": log.details}
        )
        return {"status": "Log recorded"}
    except Exception as e:
        logging.error(f"Failed to log client message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to log message: {str(e)}")