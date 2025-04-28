"""
API endpoints for Universal Recycling Purchase Order System
"""
from .orders import router as orders_router
from .order_receiving import router as order_receiving_router
from .order_attachments import router as order_attachments_router
from .order_notes import router as order_notes_router
from .order_pdf import router as order_pdf_router
from .order_queries import router as order_queries_router
from .whatsapp import router as whatsapp_router
from .auth import router as auth_router
from .html_routes import router as html_routes_router
from .lookups import router as lookups_router
from .requesters import router as requesters_router
from .supplier_lookup import router as supplier_lookup_router
from .supplier_lookup_takealot import router as supplier_lookup_takealot_router

# List of routers to be included in the main app
routers = [
    orders_router,
    order_receiving_router,
    order_attachments_router,
    order_notes_router,
    order_pdf_router,
    order_queries_router,
    whatsapp_router,
    auth_router,
    html_routes_router,
    lookups_router,
    requesters_router,
    supplier_lookup_router,
    supplier_lookup_takealot_router
]