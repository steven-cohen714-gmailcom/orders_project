# File: backend/endpoints/__init__.py

from .lookups import router as lookups_router
from .orders import router as orders_router
from .admin import admin_router
from .auth import router as auth_router
from .order_queries import router as order_queries_router
from .order_attachments import router as attachments_router
from .order_receiving import router as order_receiving_router
from .utils import router as utils_router
# NEW: Import the new draft_orders router
from . import draft_orders 

routers = [
    lookups_router,
    orders_router,
    admin_router,
    auth_router,
    order_queries_router,
    attachments_router,
    order_receiving_router,
    utils_router,
    # NEW: Add the draft_orders router to the list
    draft_orders.router 
]