from fastapi import APIRouter

# Import the full CRUD lookups router to expose under /admin
from .lookups import router as lookups_router

# Create the admin router
admin_router = APIRouter(
    tags=["admin"]
)

# Mount all CRUD endpoints under the /admin prefix
admin_router.include_router(lookups_router)
