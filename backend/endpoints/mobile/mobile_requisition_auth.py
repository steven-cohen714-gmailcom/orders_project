# File: backend/endpoints/mobile/mobile_requisition_auth.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from backend.database import get_db_connection

router = APIRouter(prefix="/mobile_requisition_auth", tags=["mobile requisition auth"])

@router.post("/login")
async def login_requisitioner(request: Request):
    try:
        data = await request.json()
        name = data.get("name", "").strip()

        if not name:
            raise HTTPException(status_code=400, detail="Name is required")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM requisitioners WHERE name = ?", (name,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Requisitioner not found")

            request.session["requisitioner_id"] = row["id"]
            request.session["requisitioner_name"] = name
            return {"message": f"Logged in as {name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}")

@router.get("/session_debug")
async def session_debug(request: Request):
    return JSONResponse(content={
        "requisitioner_id": request.session.get("requisitioner_id"),
        "requisitioner_name": request.session.get("requisitioner_name")
    })
