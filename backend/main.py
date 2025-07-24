# File: backend/main.py
# Relative Path: backend/main.py

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from backend.endpoints import html_routes
from backend.endpoints import requisitions
from backend.endpoints import requisition_attachments
from backend.endpoints.lookups import mark_cod_paid_api as mark_cod_paid_api_module
from backend.endpoints.mobile import mobile_requisition_auth
from backend.endpoints.email_service import router as email_service_router 

from pathlib import Path
import logging
import sys
import os
import sqlite3
print(f"DEBUG: Current working directory is: {os.getcwd()}") # Add this line

# --- Database ---
from backend.database import init_db, get_db_connection

# --- MODIFIED: Import permissions from backend.utils.permissions_utils ---
from backend.utils.permissions_utils import require_login, require_screen_permission 

# --- Routers ---
# REMOVED: from backend.endpoints import routers (explicitly listing now)
from backend.endpoints.mobile import mobile_auth
from backend.endpoints.mobile import mobile_requisition_auth
from backend.endpoints.mobile import mobile_requisition
from backend.endpoints.admin import admin_router # NEW/RE-ADDED: Import the main admin router
from backend.endpoints.auth import router as auth_router
from backend.endpoints.orders import router as orders_router
from backend.endpoints.new_order_pdf_generator import router as new_order_pdf_router
from backend.endpoints.pending_order_pdf_generator import router as pending_order_pdf_router
from backend.endpoints.order_queries import router as order_queries_router
from backend.endpoints.order_receiving import router as order_receiving_router
from backend.endpoints.order_attachments import router as attachments_router
from backend.endpoints.utils import router as utils_router
from backend.endpoints.mobile.mobile_awaiting_authorisation import router as mobile_auth_router
from backend.endpoints.order_notes import router as order_notes_router

# For audit trail filtering: Import the specific audit trail filters router
from backend.endpoints.audit_trail_filters import router as audit_trail_filters_router 

# --- NEW IMPORT: Import the new draft_orders router ---
from backend.endpoints import draft_orders

# Explicitly import individual routers from lookups, aliasing them to 'router'
from backend.endpoints.lookups.requisitioners import router as requisitioners_lookups_router
from backend.endpoints.lookups.requesters import router as requesters_lookups_router
from backend.endpoints.lookups.items import router as items_lookups_router
from backend.endpoints.lookups.suppliers import router as suppliers_lookups_router
from backend.endpoints.lookups.projects import router as projects_lookups_router
from backend.endpoints.lookups.settings import router as settings_lookups_router
from backend.endpoints.lookups.business_details import router as business_details_lookups_router
from backend.endpoints.lookups.users import router as users_lookups_router


# Allow scripts to import from parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.add_debug_validation_handler import install_validation_handler

# Setup logging
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/server_startup.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

try:
    init_db()
    logging.info("✅ Database initialized successfully.")
except Exception as e:
    logging.exception("❌ Failed to initialize database")
    raise

# --- FastAPI App Init ---
app = FastAPI(
    debug=True,
    title="Universal Recycling Purchase Order System",
    description="Purchase Order management system for Universal Recycling"
)

install_validation_handler(app)

# --- Static and Upload Directories ---
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/data/uploads", StaticFiles(directory="data/uploads"), name="uploads")

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="your-new-secure-key", same_site="lax", https_only=False)

templates = Jinja2Templates(directory="frontend/templates")

# --- Static Routes Router ---
static_router = APIRouter()

# For audit trail test only: New route for the test screen, bypassing permissions
@static_router.get("/audit_trail_test", response_class=HTMLResponse)
async def audit_trail_test_page(request: Request):
    return templates.TemplateResponse(
        "audit_trail_test.html",
        {"request": request}
    )

@static_router.get("/mobile/authorisations", response_class=HTMLResponse, 
                    dependencies=[Depends(require_login), Depends(require_screen_permission("my_authorisations"))]) 
async def mobile_authorisations_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "mobile/mobile_authorisations.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions
        }
    )

@static_router.get("/mobile/requisition_login", response_class=HTMLResponse)
async def mobile_requisition_login_page(request: Request):
    return templates.TemplateResponse("mobile/mobile_requisition_login.html", {"request": request})

@static_router.get("/home", response_class=HTMLResponse, 
                   dependencies=[Depends(require_login)]) 
async def home(request: Request):
    logging.info("Rendering home page")
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/orders/new", response_class=HTMLResponse, 
                    dependencies=[Depends(require_login), Depends(require_screen_permission("new_order"))])
async def new_order_page(request: Request):
    logging.info("Starting to render new order page")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
            cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
            cursor.execute("SELECT item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
            cursor.execute("SELECT project_code, project_name FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            row = cursor.fetchone()
            business_details = dict(row) if row else {
                "company_name": "Default Company",
                "address_line1": "N/A",
                "address_line2": "",
                "city": "N/A",
                "province": "N/A",
                "postal_code": "N/A",
                "telephone": "N/A",
                "vat_number": "N/A"
            }
        user_screen_permissions = request.session.get("screen_permissions", [])
        return templates.TemplateResponse("new_order.html", {
            "request": request,
            "requesters": requesters,
            "suppliers": suppliers,
            "items": items,
            "projects": projects,
            "business_details": business_details,
            "user_screen_permissions": user_screen_permissions 
        })

    except Exception as e:
        logging.error(f"Error rendering new order page: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error rendering new order page: {str(e)}")

@static_router.get("/orders/pending_orders", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("pending_orders"))])
async def pending_orders_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "pending_orders.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

# --- NEW STATIC ROUTE: for Draft Orders page ---
@static_router.get("/orders/draft_orders", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("draft_orders"))])
async def draft_orders_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "draft_orders.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )
# --- END NEW STATIC ROUTE ---

@static_router.get("/orders/cod_orders", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("cod_orders"))])
async def cod_orders_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "cod_orders.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/orders/received_orders", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("received_orders"))])
async def received_orders_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "received_orders.html",
        {

            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/orders/audit_trail", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("audit_trail"))])
async def audit_trail_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "audit_trail.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/maintenance", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("maintenance"))])
async def maintenance_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "maintenance.html",
        {

            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/orders/partially_delivered", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("partially_delivered_orders"))])
async def partially_delivered_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "partially_delivered.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/requisitions/pending_requisitions", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("pending_requisitions"))])
async def pending_requisitions_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "pending_requisitions.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/requisitions/new", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("new_requisition"))])
async def new_requisition_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "new_requisition.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/favicon.ico")
async def favicon():
    favicon_path = Path("frontend/static/favicon.ico")
    if not favicon_path.exists():
        return {"error": "Favicon not found"}, 404
    try:
        with open(favicon_path, "rb") as f:
            content = f.read()
        return Response(content=content, media_type="image/x-icon")
    except Exception as e:
        logging.error(f"Error serving favicon: {str(e)}", exc_info=True)
        return {"error": "Failed to serve favicon"}, 500
    
@static_router.get("/orders/authorisations_per_user", 
                   response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("my_authorisations"))])
async def authorisations_per_user_page(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "authorisations_per_user.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions 
        }
    )

@static_router.get("/mobile/requisition", response_class=HTMLResponse) 
async def mobile_requisition_form(request: Request):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "mobile/mobile_requisition.html",
        {
            "request": request,
            "user_screen_permissions": user_screen_permissions
        }
    )

# --- RE-ADDED: Static Routes for Admin Edit Order Search ---
@static_router.get("/admin/edit_order_search", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("edit_order_admin"))])
async def edit_order_search_page(request: Request, error_message: str = None):
    user_screen_permissions = request.session.get("screen_permissions", [])
    return templates.TemplateResponse(
        "admin/edit_order_search.html",
        {
            "request": request,
            "error_message": error_message,
            "user_screen_permissions": user_screen_permissions
        }
    )

@static_router.post("/admin/edit_order_search", response_class=HTMLResponse,
                    dependencies=[Depends(require_login), Depends(require_screen_permission("edit_order_admin"))])
async def handle_edit_order_search(request: Request):
    form_data = await request.form()
    order_identifier = form_data.get("order_identifier")

    if not order_identifier:
        return await edit_order_search_page(request, error_message="Please enter an Order Number or ID.")

    try:
        # Assuming order_identifier could be "URCXXX" or just "XXX"
        # Extract the numeric part
        order_id_str = order_identifier.replace("URC", "").strip()
        order_id = int(order_id_str)
        
        # Redirect to the actual edit page with the order_id
        return RedirectResponse(url=f"/admin/edit_order/{order_id}", status_code=303)
    except ValueError:
        return await edit_order_search_page(request, error_message="Invalid Order ID. Please enter a number or 'URC' followed by a number.")
    except Exception as e:
        logging.error(f"Error handling order search: {e}", exc_info=True)
        return await edit_order_search_page(request, error_message=f"An unexpected error occurred: {e}")

# RE-ADDED: Direct access to edit order page via ID (GET)
@static_router.get("/admin/edit_order/{order_id}", response_class=HTMLResponse,
                   dependencies=[Depends(require_login), Depends(require_screen_permission("edit_order_admin"))])
async def edit_order_page(request: Request, order_id: int):
    user_screen_permissions = request.session.get("screen_permissions", [])
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()

        # Fetch order details
        cursor.execute("""
            SELECT o.id, o.order_number, o.status, o.created_date, o.total,
                   o.order_note, o.note_to_supplier, o.supplier_id, o.requester_id,
                   o.payment_terms, o.last_modified_by_user_id,
                   s.name AS supplier_name, r.name AS requester_name
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN requesters r ON o.requester_id = r.id
            WHERE o.id = ?
        """, (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")

        # Fetch order items
        cursor.execute("""
            SELECT id, item_code, item_description, project, qty_ordered, price, total
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        order_items = [dict(row) for row in cursor.fetchall()]

        # Fetch all lookup data for dropdowns
        cursor.execute("SELECT id, name FROM requesters ORDER BY name")
        requesters = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT id, name, account_number FROM suppliers ORDER BY name")
        suppliers = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT id, item_code, item_description FROM items ORDER BY item_code")
        items = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT id, project_code, project_name FROM projects ORDER BY project_code")
        projects = [dict(row) for row in cursor.fetchall()]

        logging.info(f"Rendering edit_order page for Order ID: {order_id}")
        return templates.TemplateResponse(
            "admin/edit_order.html",
            {
                "request": request,
                "order": dict(order), # Pass the 'order' dictionary
                "order_items": order_items,
                "requesters": requesters,
                "suppliers": suppliers,
                "items": items,
                "projects": projects,
                "user_screen_permissions": user_screen_permissions 
            }
        )
    except Exception as e:
        logging.error(f"Error loading edit_order page for Order ID {order_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to load order for editing: {str(e)}")
    finally:
        conn.close()

# --- END RE-ADDED: Static Routes for Admin Edit Order Search ---

# --- Include Routers (ORDER IS CRITICAL) ---
# Start with static routes and general authentication
app.include_router(static_router)
app.include_router(auth_router)
app.include_router(mobile_auth.router)
app.include_router(mobile_requisition_auth.router)
app.include_router(mobile_requisition.router)
app.include_router(html_routes.router) # Generic HTML routes

# Include all specific lookup routers first, as they often have static paths
app.include_router(requisitioners_lookups_router, prefix="/lookups")
app.include_router(requesters_lookups_router, prefix="/lookups")
app.include_router(items_lookups_router, prefix="/lookups")
app.include_router(suppliers_lookups_router, prefix="/lookups")
app.include_router(projects_lookups_router, prefix="/lookups")
app.include_router(settings_lookups_router, prefix="/lookups")
app.include_router(business_details_lookups_router, prefix="/lookups")
app.include_router(users_lookups_router, prefix="/lookups")

# Then more specific API routes, especially those with parameters
app.include_router(mobile_auth_router) # This router contains /orders/api/awaiting_authorisation
app.include_router(audit_trail_filters_router, prefix="/orders/api") 
app.include_router(new_order_pdf_router, prefix="/orders/api")
app.include_router(pending_order_pdf_router, prefix="/orders/api")
app.include_router(order_queries_router, prefix="/orders/api") 

# Now the draft_orders router, as it contains a general parameterized route that caused issues
app.include_router(draft_orders.router, prefix="/draft_orders")

# Other main application routers
app.include_router(orders_router, prefix="/orders")
app.include_router(attachments_router, prefix="/orders")
app.include_router(order_receiving_router, prefix="/orders")
app.include_router(order_notes_router)
app.include_router(mark_cod_paid_api_module.router, prefix="/orders")

# Requisition related routers
app.include_router(requisitions.router)
app.include_router(requisition_attachments.router, prefix="/requisitions")

# Utilities and admin
app.include_router(utils_router)
# Admin router inclusion with its prefix
# --- MODIFIED LINE BELOW ---
app.include_router(admin_router, prefix="/admin") # REMOVED dependencies=[Depends(require_login)]
app.include_router(email_service_router)


# --- Dev CLI ---
if __name__ == "__main__":
    import uvicorn
    try:
        logging.info("🚀 Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8004)
    except Exception as e:
        logging.exception("❌ Server failed to start")
        raise