from fastapi import APIRouter, Request, HTTPException
from backend.database import get_db_connection
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username", "").strip().lower()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row["username"].strip().lower() for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if username in users:
        request.session["user"] = username
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid username")

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
