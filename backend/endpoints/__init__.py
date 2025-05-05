from .lookups import router as lookups_router
from .orders import router as orders_router
from .admin import admin_router
from .auth import router as auth_router
from .order_queries import router as order_queries_router
from .order_pdf import router as pdf_router

routers = [
    lookups_router,
    orders_router,
    admin_router,
    auth_router,
    order_queries_router,
    pdf_router
]
