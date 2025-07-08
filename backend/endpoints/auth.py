from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
import bcrypt
import json
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

    username = data.get("username", "").strip().lower()
    password = data.get("password", "")

    if not username or not password:
        return JSONResponse(status_code=400, content={"error": "Username and password are required"})

    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, password_hash, rights, auth_threshold_band FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            conn.close()
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        stored_hash = user["password_hash"]
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            conn.close()
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        user_id = user["id"]
        cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user_id,))
        screen_permissions = [row["screen_code"] for row in cursor.fetchall()]
        
        conn.close()

        request.session["user"] = {
            "id": user["id"],
            "username": user["username"],
            "rights": user["rights"] or "view",
            "auth_threshold_band": user["auth_threshold_band"]
        }
        request.session["screen_permissions"] = screen_permissions 

        request.session["roles"] = user["rights"] or "view"

        # --- MODIFIED: Return screen_permissions in the JSON response ---
        return JSONResponse(
            status_code=200, 
            content={
                "success": True,
                "authorized_screens": screen_permissions # ADDED THIS LINE
            }
        )

    except Exception as e:
        print(f"Login error: {e}")
        return JSONResponse(status_code=500, content={"error": f"Login failed due to server error: {str(e)}"})

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return JSONResponse(status_code=200, content={"message": "Logged out successfully"})

@router.get("/session_debug")
async def session_debug(request: Request):
    return JSONResponse(content={
        "user": request.session.get("user"),
        "roles": request.session.get("roles"),
        "screen_permissions": request.session.get("screen_permissions")
    })