# backend/auth.py

from fastapi import APIRouter, Request, Form, Response, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
DB_PATH = "data/orders.db"


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash, rights FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user_id, pw_hash, rights = user

        # Dummy check: skip real password checking for now
        # Replace this with hashed check later
        if password != "password":
            raise HTTPException(status_code=401, detail="Incorrect password")

        request.session["user_id"] = user_id
        request.session["username"] = username
        request.session["rights"] = rights

        return RedirectResponse(url="/", status_code=302)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {e}")


@router.get("/logout")
def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@router.get("/")
def home(request: Request):
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("home.html", {"request": request, "username": username})

