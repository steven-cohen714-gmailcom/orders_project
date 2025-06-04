# File: test_items_dropdown/app.py

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sqlite3

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "orders.db"

# Serve static assets (JS, CSS) from /static/
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

@app.get("/")
def serve_main_page():
    return FileResponse(BASE_DIR / "test_item_dropdown.html")

@app.get("/items")
def get_items():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_code, item_description FROM items")
        rows = cursor.fetchall()
    return [
        {"id": row[0], "item_code": row[1], "item_description": row[2]}
        for row in rows
    ]
