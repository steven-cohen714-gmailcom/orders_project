# File: backend/utils/permissions_utils.py

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")

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
