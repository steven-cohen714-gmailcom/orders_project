# File: backend/endpoints/admin.py

from fastapi import APIRouter

# Import the full CRUD lookups router to expose under /admin
from .lookups import router as lookups_router
# NEW: Import the edit_order router
from .admin import router as admin_edit_order_router 

# Create the admin router
admin_router = APIRouter(
    tags=["admin"]
)

# Mount all CRUD endpoints under the /admin prefix
admin_router.include_router(lookups_router)
# NEW: Include the edit_order router
admin_router.include_router(admin_edit_order_router)

