from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
import bcrypt
import json
import sqlite3
import logging # Added for more specific logging in this file

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Configure logging for this specific router if needed, or use root logger
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def root_redirect_to_login():
    """Redirects the root URL to the login page."""
    return RedirectResponse(url="/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Displays the login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
    except Exception:
        logger.warning("Invalid JSON payload received for login.")
        return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

    username = data.get("username", "").strip().lower()
    password = data.get("password", "")

    if not username or not password:
        logger.warning(f"Missing username or password for login attempt by {username}.")
        return JSONResponse(status_code=400, content={"error": "Username and password are required"})

    conn = None # Initialize conn outside try block for finally
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
            logger.info(f"Failed login attempt for username: {username} - User not found.")
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        stored_hash = user["password_hash"]
        # Ensure stored_hash is a string before encoding
        if not isinstance(stored_hash, str):
            logger.error(f"Password hash for user {username} is not a string. Type: {type(stored_hash)}")
            return JSONResponse(status_code=500, content={"error": "Server configuration error."})

        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            logger.info(f"Failed login attempt for username: {username} - Incorrect password.")
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})

        user_id = user["id"]
        # --- CRITICAL FIX: Ensure screen_permissions are correctly fetched and stored ---
        cursor.execute("SELECT screen_code FROM screen_permissions WHERE user_id = ?", (user_id,))
        # Convert fetched rows to a list of screen_code strings
        screen_permissions = [row["screen_code"] for row in cursor.fetchall()]

        # Store user details and permissions in session
        request.session["user"] = {
            "id": user["id"],
            "username": user["username"],
            "rights": user["rights"] or "view", # Fallback to "view" if rights is None/empty
            "auth_threshold_band": user["auth_threshold_band"]
        }
        request.session["screen_permissions"] = screen_permissions
        request.session["roles"] = user["rights"] or "view" # Maintain 'roles' for backward compatibility if needed by old parts

        logger.info(f"User {username} logged in successfully. Permissions: {screen_permissions}")
        
        # Determine redirect URL based on permissions
        # This logic is likely handled by frontend login.js after receiving authorized_screens
        # So, we return the data needed by login.js
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "redirect_url": "/home", # Default redirect, frontend might override based on screens
                "authorized_screens": screen_permissions # Send permissions to frontend for client-side routing
            }
        )

    except Exception as e:
        logger.exception(f"Unexpected error during login for user {username}: {e}")
        return JSONResponse(status_code=500, content={"error": f"Login failed due to server error: {str(e)}"})
    finally:
        if conn:
            conn.close()

@router.get("/logout")
async def logout(request: Request):
    logger.info(f"User {request.session.get('user',{}).get('username', 'unknown')} logged out.")
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

@router.get("/session_debug")
async def session_debug(request: Request):
    logger.debug(f"Session debug requested. Session content: {request.session}")
    return JSONResponse(content={
        "user": request.session.get("user"),
        "roles": request.session.get("roles"),
        "screen_permissions": request.session.get("screen_permissions")
    })