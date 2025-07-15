# File: backend/utils/permissions_utils.py

from fastapi import Request, HTTPException, Depends # Added Depends for require_screen_permission
from fastapi.responses import HTMLResponse, RedirectResponse # Added RedirectResponse
from fastapi.templating import Jinja2Templates
import logging 

templates = Jinja2Templates(directory="frontend/templates")

# MODIFIED: require_login now returns the user dictionary
def require_login(request: Request):
    """
    Dependency to ensure a user is logged in and provides the user session data.
    Redirects to login page if not authenticated.
    """
    user = request.session.get("user")
    if not user:
        # Log this redirect for debugging
        logging.warning(f"Unauthorized access attempt. Redirecting to login.")
        raise HTTPException(status_code=302, headers={"Location": "/"})
    return user # <--- CRITICAL CHANGE: Return the user dictionary

def require_screen_permission(screen_code: str):
    """
    Dependency to check if the logged-in user has permission for a specific screen.
    Raises 403 HTTPException if not authorized.
    """
    def _check_permission(request: Request):
        if not request.session.get("user"):
            # If not logged in, redirect to login page (or raise 401)
            raise HTTPException(status_code=302, headers={"Location": "/"}) 
        
        user_permissions = request.session.get("screen_permissions", [])
        
        if screen_code not in user_permissions:
            logging.warning(f"User {request.session.get('user',{}).get('username')} attempted to access {screen_code} without permission.")
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to view this page. Missing required screen permission."
            )
        return True 
    return _check_permission

# Original function, kept for completeness if used elsewhere
def enforce_roles(request: Request, allowed_roles: list):
    """
    Checks if the user has at least one of the allowed roles.
    Returns None if allowed. Returns access_denied TemplateResponse if not.
    """
    roles = request.session.get("roles", "")
    role_set = {r.strip().lower() for r in roles.split(",")}

    if not any(role in role_set for role in allowed_roles):
        return templates.TemplateResponse("access_denied.html", {"request": request})

    return None