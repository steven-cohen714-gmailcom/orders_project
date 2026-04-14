from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
import bcrypt
import sqlite3
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Router-specific logger (inherits config from root logger)
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def root_redirect_to_login():
    """Redirect the root URL to the login page."""
    return RedirectResponse(url="/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request):
    # --- Parse input ---
    try:
        data = await request.json()
    except Exception:
        logger.warning("Invalid JSON payload received for login.")
        return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

    username = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not password:
        logger.warning("Missing username or password for login attempt.")
        return JSONResponse(status_code=400, content={"error": "Username and password are required"})

    conn = None
    try:
        # --- Load user record (case-insensitive) ---
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                rights,
                auth_threshold_band,
                email,
                COALESCE(can_delete_transactions, 0)  AS can_delete_transactions,
                COALESCE(can_edit_draft_orders, 0)     AS can_edit_draft_orders
            FROM users
            WHERE LOWER(username) = ?
            """,
            (username,)
        )
        user = cursor.fetchone()
        if not user:
            logger.info(f"Failed login attempt for username: {username} - User not found.")
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        stored_hash = user["password_hash"]
        if not isinstance(stored_hash, str):
            logger.error(f"Password hash for user {username} has unexpected type: {type(stored_hash)}")
            return JSONResponse(status_code=500, content={"error": "Server configuration error"})

        # --- Verify password ---
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            logger.info(f"Failed login attempt for username: {username} - Incorrect password.")
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        # --- Fetch screen permissions ---
        cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user["id"],))
        screen_permissions = [row["screen_code"] for row in cursor.fetchall()]

        # --- Build session payload (store flags as 0/1 ints) ---
        session_user = {
            "id": user["id"],
            "username": user["username"],
            "rights": user["rights"] or "view",
            "auth_threshold_band": user["auth_threshold_band"],
            "email": user["email"],
            "can_delete_transactions": 1 if (user["can_delete_transactions"] or 0) else 0,
            "can_edit_draft_orders": 1 if (user["can_edit_draft_orders"] or 0) else 0,
        }
        request.session["user"] = session_user
        request.session["screen_permissions"] = screen_permissions
        request.session["roles"] = session_user["rights"]  # backward-compat key some legacy code uses

        logger.info(
            "User %s logged in successfully. Perms=%s | Flags(delete=%s, edit_drafts=%s)",
            session_user["username"],
            screen_permissions,
            session_user["can_delete_transactions"],
            session_user["can_edit_draft_orders"],
        )

        # Frontend decides where to go based on authorized_screens; keep default
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "redirect_url": "/home",
                "authorized_screens": screen_permissions,
            },
        )

    except Exception as e:
        logger.exception("Unexpected error during login for user %s: %s", username, e)
        return JSONResponse(status_code=500, content={"error": "Login failed due to server error"})
    finally:
        if conn:
            conn.close()

@router.get("/logout")
async def logout(request: Request):
    username = request.session.get("user", {}).get("username", "unknown")
    logger.info("User %s logged out.", username)
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

@router.get("/session_debug")
async def session_debug(request: Request):
    logger.debug("Session debug requested.")
    return JSONResponse(
        content={
            "user": request.session.get("user"),
            "roles": request.session.get("roles"),
            "screen_permissions": request.session.get("screen_permissions"),
        }
    )
