from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from backend.endpoints import routers
from backend.endpoints.admin import admin_router
from backend.endpoints.order_pdf import router as pdf_router
from backend.endpoints.auth import router as auth_router
from backend.endpoints.order_queries import router as order_queries_router
from backend.endpoints.orders import router as orders_router
from backend.endpoints.order_attachments import router as attachments_router
from backend.endpoints.pdf_generator import router as pdf_generator_router
from backend.endpoints.order_receiving import router as order_receiving_router

from backend.database import init_db, get_db_connection
from pathlib import Path
import logging
import sys
import os

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
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

templates = Jinja2Templates(directory="frontend/templates")

# --- Static Routes Router (to take precedence over dynamic routes) ---
static_router = APIRouter()

@static_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logging.info("Rendering login page")
    return templates.TemplateResponse("login.html", {"request": request})

@static_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/")
    logging.info("Rendering home page")
    return templates.TemplateResponse("home.html", {"request": request})

@static_router.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request):
    logging.info("Starting to render new order page")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
            logging.info(f"Requesters fetched: {requesters}")
            cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
            logging.info(f"Suppliers fetched: {suppliers}")
            cursor.execute("SELECT item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
            logging.info(f"Items fetched: {items}")
            cursor.execute("SELECT project_code, project_name FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
            logging.info(f"Projects fetched: {projects}")
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            row = cursor.fetchone()
            if not row:
                logging.error("No business details found in database")
                business_details = {
                    "company_name": "Default Company",
                    "address_line1": "N/A",
                    "address_line2": "",
                    "city": "N/A",
                    "province": "N/A",
                    "postal_code": "N/A",
                    "telephone": "N/A",
                    "vat_number": "N/A"
                }
            else:
                business_details = dict(row)
            logging.info(f"Business details fetched: {business_details}")

        template_context = {
            "request": request,
            "requesters": requesters,
            "suppliers": suppliers,
            "items": items,
            "projects": projects,
            "business_details": business_details
        }
        logging.info(f"Template context: {template_context}")
        
        response = templates.TemplateResponse("new_order.html", template_context)
        logging.info("Successfully rendered new_order.html")
        return response
    except Exception as e:
        logging.error(f"Error rendering new order page: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error rendering new order page: {str(e)}")

@static_router.get("/orders/pending_orders", response_class=HTMLResponse)
async def pending_orders_page(request: Request):
    logging.info("Rendering pending orders page")
    return templates.TemplateResponse("pending_orders.html", {"request": request})

@static_router.get("/orders/received_orders", response_class=HTMLResponse)
async def received_orders_page(request: Request):
    logging.info("Rendering received orders page")
    return templates.TemplateResponse("received_orders.html", {"request": request})

@static_router.get("/orders/audit_trail", response_class=HTMLResponse)
async def audit_trail_page(request: Request):
    logging.info("Rendering audit trail page")
    return templates.TemplateResponse("audit_trail.html", {"request": request})

@static_router.get("/maintenance", response_class=HTMLResponse)
async def maintenance_page(request: Request):
    logging.info("Rendering maintenance page")
    return templates.TemplateResponse("maintenance.html", {"request": request})

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

# --- Include Routers ---
# Include static routes first to take precedence
app.include_router(static_router)

# Include other routers after static routes
for router in routers:
    app.include_router(router, prefix="/lookups")
app.include_router(admin_router, prefix="/admin")
app.include_router(order_queries_router)
app.include_router(pdf_router)
app.include_router(auth_router)
app.include_router(orders_router, prefix="/orders")
app.include_router(attachments_router, prefix="/orders")
app.include_router(pdf_generator_router)
app.include_router(order_receiving_router, prefix="/orders")

# --- Dev CLI (if needed) ---
if __name__ == "__main__":
    import uvicorn
    try:
        logging.info("🚀 Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8004)
    except Exception as e:
        logging.exception("❌ Server failed to start")
        raise