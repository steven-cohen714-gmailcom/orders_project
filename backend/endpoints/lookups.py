from fastapi import APIRouter, HTTPException
import sqlite3
from pathlib import Path
from datetime import datetime
import json

router = APIRouter()

def log_lookup(endpoint: str, outcome: str, detail: str = ""):
    log_path = Path("logs/lookups_log.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        entry = {"time": timestamp, "endpoint": endpoint, "status": outcome}
        if detail:
            entry["detail"] = detail
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

@router.get("/suppliers")
def get_suppliers():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, account_number, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
        log_lookup("/suppliers", "success")
        return {"suppliers": suppliers}
    except Exception as e:
        log_lookup("/suppliers", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load suppliers: {e}")

@router.get("/requesters")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
        log_lookup("/requesters", "success")
        return {"requesters": requesters}
    except Exception as e:
        log_lookup("/requesters", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load requesters: {e}")

@router.get("/items")
def get_items():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
        log_lookup("/items", "success")
        return {"items": items}
    except Exception as e:
        log_lookup("/items", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load items: {e}")

@router.get("/projects")
def get_projects():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT project_code, project_name FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
        log_lookup("/projects", "success")
        return {"projects": projects}
    except Exception as e:
        log_lookup("/projects", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load projects: {e}")
