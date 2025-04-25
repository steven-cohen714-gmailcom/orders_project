from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/orders/new", response_class=HTMLResponse)
def show_new_order_form(request: Request):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
            cursor.execute("SELECT id, item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
            cursor.execute("SELECT id, project_code FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
        return templates.TemplateResponse(
            "new_order.html",
            {"request": request, "suppliers": suppliers, "items": items, "projects": projects}
        )
    except Exception as e:
        print(f"Error fetching data: {e}")
        return templates.TemplateResponse(
            "new_order.html",
            {"request": request, "suppliers": [], "items": [], "projects": []}
        )

@router.get("/orders/pending", response_class=HTMLResponse)
def show_pending_orders(request: Request):
    return templates.TemplateResponse("pending_orders.html", {"request": request})