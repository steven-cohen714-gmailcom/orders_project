from .requesters import router as requesters_router
from .suppliers import router as suppliers_router
from .items import router as items_router
from .projects import router as projects_router
from .settings import router as settings_router
from .business_details import router as business_details_router
from .users import router as users_router

# Aggregate all lookup routers into a single router
from fastapi import APIRouter

router = APIRouter()

# Include individual routers without additional prefixes
router.include_router(requesters_router)
router.include_router(suppliers_router)
router.include_router(items_router)
router.include_router(projects_router)
router.include_router(settings_router)
router.include_router(business_details_router)
router.include_router(users_router)