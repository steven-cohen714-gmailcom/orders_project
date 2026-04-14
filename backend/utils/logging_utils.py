from __future__ import annotations
import logging, os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict

# -------- Config (override via env if you like) --------
REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = Path(os.getenv("LOG_DIR") or (REPO_ROOT / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

# rotate ~5MB, keep 5 files (override via env)
ROTATE_BYTES = int(os.getenv("LOG_ROTATE_BYTES") or 5_000_000)
BACKUP_COUNT = int(os.getenv("LOG_BACKUPS") or 5)
DEFAULT_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)

FMT = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

# Map “channels” to filenames. Add more as you migrate modules.
CHANNELS: Dict[str, str] = {
    "app":              "app.log",
    "db":               "db_activity_log.txt",
    "email_dispatch":   "email_dispatch_log.txt",
    "email_transport":  "email_transport_log.txt",
    "authorisations":   "authorisations_log.txt",
    "access":           "access.log",              # if you add request logging later
}

# cache of configured loggers
_LOGGERS: Dict[str, logging.Logger] = {}

def _attach_file_handler(logger: logging.Logger, filepath: Path, level: int) -> None:
    logger.setLevel(level)
    logger.propagate = False  # don’t double-log to root/uvicorn
    abs_path = str(filepath.resolve())
    already = any(getattr(h, "baseFilename", None) == abs_path for h in logger.handlers)
    if not already:
        fh = RotatingFileHandler(abs_path, maxBytes=ROTATE_BYTES, backupCount=BACKUP_COUNT)
        fh.setLevel(level)
        fh.setFormatter(FMT)
        logger.addHandler(fh)

def get_logger(channel: str, *, level: int = DEFAULT_LEVEL) -> logging.Logger:
    """
    Return a configured logger for a logical channel (file).
    Unknown channels fall back to app.log.
    """
    name = channel.strip().lower()
    if name in _LOGGERS:
        return _LOGGERS[name]

    filename = CHANNELS.get(name, CHANNELS["app"])
    logger = logging.getLogger(name)
    _attach_file_handler(logger, LOG_DIR / filename, level)
    _LOGGERS[name] = logger
    return logger

# Optional: call once early if you want a console mirror during dev
def enable_console_logging(level: int = DEFAULT_LEVEL) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(FMT)
        root.addHandler(ch)
