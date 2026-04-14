# File: backend/utils/permissions_utils.py
# Relative Path: backend/utils/permissions_utils.py

from fastapi import Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
import logging
import json

# Configure logging specifically for this module to ensure debug messages are seen
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture detailed logs

templates = Jinja2Templates(directory="frontend/templates")


def _coerce_session_user(raw):
    """
    Session 'user' may be a dict or a JSON string. Normalize to dict.
    """
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            logger.debug("Failed to json.loads(session['user']); leaving as empty dict.")
            return {}
    return {}


def _truthy(v) -> bool:
    """
    Accepts 1/0, True/False, '1'/'0', 'true'/'false', etc.
    """
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        return v.strip().lower() in {"1", "true", "yes", "on"}
    return False


def require_login(request: Request):
    """
    Dependency to ensure a user is logged in and provides the user session data.
    Redirects to login page if not authenticated.
    """
    raw_user = request.session.get("user")
    if not raw_user:
        logger.warning("Unauthorized access attempt. Redirecting to login.")
        # Use 302 redirect like your existing code-paths expect.
        raise HTTPException(status_code=302, headers={"Location": "/"})

    user = _coerce_session_user(raw_user)

    # --- minimal addition: ensure 'review_orders' is present so the tab shows ---
    try:
        perms = request.session.get("screen_permissions", [])
        if "review_orders" not in perms:
            perms = list(perms) + ["review_orders"]
            request.session["screen_permissions"] = perms
            logger.debug("Added 'review_orders' to session screen_permissions.")
    except Exception as e:
        # Never block login on this; just log
        logger.debug(f"Could not ensure 'review_orders' permission: {e}")

    return user


def require_screen_permission(screen_code: str):
    """
    Dependency to check if the logged-in user has permission for a specific screen.
    Raises 403 HTTPException if not authorized.
    """
    def _check_permission(
        request: Request,
        user: dict = Depends(require_login),
    ):
        logger.debug(f"Permissions check for screen_code: '{screen_code}' initiated.")
        logger.debug(f"User object in session: {user}")

        username = user.get('username', 'N/A')
        user_permissions = request.session.get("screen_permissions", [])
        logger.debug(f"User '{username}' (ID: {user.get('id', 'N/A')}) has permissions: {user_permissions}")

        if screen_code not in user_permissions:
            logger.warning(
                f"User '{username}' attempted to access '{screen_code}' without permission. "
                f"Current permissions: {user_permissions}"
            )
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view this page. Missing required screen permission."
            )
        logger.debug(f"User '{username}' successfully authorized for '{screen_code}'.")
        return True

    return _check_permission


def require_can_edit_draft_orders(
    request: Request,
    user: dict = Depends(require_login),
):
    """
    Dependency to enforce the 'can_edit_draft_orders' flag on any draft-editing actions.
    Returns True if allowed, raises 403 otherwise.
    """
    if not user or not user.get("id"):
        raise HTTPException(status_code=302, headers={"Location": "/"})

    if not _truthy(user.get("can_edit_draft_orders")):
        username = user.get("username", "unknown")
        logger.warning(f"User '{username}' attempted to edit draft orders without permission.")
        raise HTTPException(status_code=403, detail="Not allowed to edit draft orders")

    return True


def enforce_roles(request: Request, allowed_roles: list):
    """
    Checks if the user has at least one of the allowed roles.
    Returns None if allowed. Returns access_denied TemplateResponse if not.
    """
    roles = request.session.get("roles", "")
    role_set = {r.strip().lower() for r in roles.split(",")}

    if not any(role in role_set for role in allowed_roles):
        logger.warning(
            f"User {request.session.get('user', {}).get('username', 'unknown')} denied access based on roles. "
            f"Required: {allowed_roles}, Has: {role_set}"
        )
        return templates.TemplateResponse("access_denied.html", {"request": request})

    return None
