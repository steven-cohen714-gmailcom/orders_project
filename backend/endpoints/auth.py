from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
import bcrypt
import json

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, rights, auth_threshold_band FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        stored_hash = user["password_hash"]
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        request.session["user"] = json.dumps({
            "id": user["id"],
            "username": user["username"],
            "rights": user["rights"],
            "auth_threshold_band": user["auth_threshold_band"]
        })

        return RedirectResponse("/orders/pending_orders", status_code=302)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed due to server error: {str(e)}")

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
