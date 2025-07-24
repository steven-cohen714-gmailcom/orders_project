# File: backend/endpoints/admin/__init__.py
# This file now acts as the main router for the 'admin' package.

from fastapi import APIRouter

# Import the full CRUD lookups router to expose under /admin
# The '..' indicates going up one level from 'admin' directory to 'endpoints'
# and then down into 'lookups'.
from ..lookups import router as lookups_router

# Import the edit_order router from within the 'admin' package itself.
# The '.' indicates looking within the current package ('admin').
from .edit_order import router as admin_edit_order_router

# Create the main admin router
admin_router = APIRouter(
    tags=["admin"]
)

# Mount all CRUD endpoints from lookups under the /admin prefix
admin_router.include_router(lookups_router)

# Include the edit_order router under the /admin prefix
admin_router.include_router(admin_edit_order_router)
