# backend/endpoints/mobile/mobile_auth.py

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from backend.database import get_db_connection

router = APIRouter()


@router.post("/mobile/login")
async def mobile_login(request: Request, username: str = Form(...), password: str = Form(...)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if not user:
            return RedirectResponse("/mobile/login?error=1", status_code=302)
        request.session["user"] = {
            "username": user["username"],
            "auth_threshold_band": user["auth_threshold_band"],
        }
    return RedirectResponse("/mobile/authorisations", status_code=302)


@router.get("/mobile/logout")
async def mobile_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/mobile/login", status_code=302)


@router.get("/mobile/get_user_info")
async def get_user_info(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return JSONResponse(content=user)
