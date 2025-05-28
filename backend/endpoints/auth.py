from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
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
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, rights, auth_threshold_band FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        stored_hash = user["password_hash"]
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        user_roles = user["rights"] or "view"

        request.session["user"] = {
            "id": user["id"],
            "username": user["username"],
            "rights": user_roles,
            "auth_threshold_band": user["auth_threshold_band"]
        }

        # Assign session roles from DB
        request.session["roles"] = user_roles

        return JSONResponse(status_code=200, content={"success": True})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Login failed due to server error: {str(e)}"})

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return JSONResponse(status_code=200, content={"message": "Logged out successfully"})

@router.get("/session_debug")
async def session_debug(request: Request):
    return JSONResponse(content={
        "user": request.session.get("user"),
        "roles": request.session.get("roles")
    })
