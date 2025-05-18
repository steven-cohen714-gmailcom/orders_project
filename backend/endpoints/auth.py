from fastapi import APIRouter, Request, HTTPException
from backend.database import get_db_connection
from fastapi.responses import RedirectResponse
import json

router = APIRouter()

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
        cursor.execute("SELECT id, username, password_hash, rights, auth_threshold_band FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        stored_password = user["password_hash"]
        if password != stored_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # ✅ Store entire user object in session as JSON
        request.session["user"] = json.dumps({
            "id": user["id"],
            "username": user["username"],
            "auth_threshold_band": user["auth_threshold_band"],
            "rights": user["rights"]
        })

        return {"message": "Login successful"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
