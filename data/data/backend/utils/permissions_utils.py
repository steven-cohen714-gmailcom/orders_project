# File: backend/utils/permissions_utils.py

from fastapi import Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging

# Configure logging specifically for this module to ensure debug messages are seen
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set to DEBUG to capture detailed logs

templates = Jinja2Templates(directory="frontend/templates")

def require_login(request: Request):
    """
    Dependency to ensure a user is logged in and provides the user session data.
    Redirects to login page if not authenticated.
    """
    user = request.session.get("user")
    if not user:
        # Log this redirect for debugging
        logger.warning(f"Unauthorized access attempt. Redirecting to login.")
        raise HTTPException(status_code=302, headers={"Location": "/"})
    return user

def require_screen_permission(screen_code: str):
    """
    Dependency to check if the logged-in user has permission for a specific screen.
    Raises 403 HTTPException if not authorized.
    """
    def _check_permission(request: Request):
        user = request.session.get("user")
        
        # --- START DEBUG LOGGING ---
        logger.debug(f"Permissions check for screen_code: '{screen_code}' initiated.")
        logger.debug(f"User object in session: {user}")
        
        if not user:
            logger.warning("Permissions check failed: User not found in session. Redirecting to login.")
            raise HTTPException(status_code=302, headers={"Location": "/"})
        
        username = user.get('username', 'N/A')
        user_permissions = request.session.get("screen_permissions", [])
        
        logger.debug(f"User '{username}' (ID: {user.get('id', 'N/A')}) has permissions: {user_permissions}")
        # --- END DEBUG LOGGING ---
        
        if screen_code not in user_permissions:
            logger.warning(f"User '{username}' attempted to access '{screen_code}' without permission. Current permissions: {user_permissions}")
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view this page. Missing required screen permission."
            )
        logger.debug(f"User '{username}' successfully authorized for '{screen_code}'.")
        return True
    return _check_permission

def enforce_roles(request: Request, allowed_roles: list):
    """
    Checks if the user has at least one of the allowed roles.
    Returns None if allowed. Returns access_denied TemplateResponse if not.
    """
    roles = request.session.get("roles", "")
    role_set = {r.strip().lower() for r in roles.split(",")}

    if not any(role in role_set for role in allowed_roles):
        logger.warning(f"User {request.session.get('user',{}).get('username', 'unknown')} denied access based on roles. Required: {allowed_roles}, Has: {role_set}")
        return templates.TemplateResponse("access_denied.html", {"request": request})

    return None