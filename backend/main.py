from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from backend.endpoints.lookups import router as lookups_router
from backend.endpoints.orders import router as orders_router
from backend.endpoints.order_queries import router as order_queries_router
from backend.database import init_db, get_db_connection
from pathlib import Path
import logging
import sys
import os

# Ensure backend directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Install debug validator
from scripts.add_debug_validation_handler import install_validation_handler

# Logging setup
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/server_startup.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Initialize DB
try:
    init_db()
    logging.info("✅ Database initialized successfully.")
except Exception as e:
    logging.exception("❌ Failed to initialize database")
    raise

# FastAPI app
app = FastAPI(
    title="Universal Recycling Purchase Order System",
    description="Purchase Order management system for Universal Recycling"
)

# Enhanced validation
install_validation_handler(app)

# Mount folders
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/data/uploads", StaticFiles(directory="data/uploads"), name="uploads")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Include routers with explicit precedence
app.include_router(lookups_router, prefix="/lookups")
app.include_router(order_queries_router)  # Add this line to include order_queries router
app.include_router(orders_router, prefix="/orders")

# HTML routes using Jinja2 templates
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Fetch requesters
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
            # Fetch suppliers
            cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
            # Fetch items
            cursor.execute("SELECT item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
            # Fetch projects
            cursor.execute("SELECT project_code, project_name FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
            # Fetch business details
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            row = cursor.fetchone()
            if not row:
                logging.error("No business details found in database")
                raise HTTPException(status_code=500, detail="No business details found in database")
            business_details = dict(row)
            logging.info(f"Business details fetched: {business_details}")

        return templates.TemplateResponse("new_order.html", {
            "request": request,
            "requesters": requesters,
            "suppliers": suppliers,
            "items": items,
            "projects": projects,
            "business_details": business_details
        })
    except Exception as e:
        logging.error(f"Error rendering new order page: {str(e)}")
        raise

@app.get("/orders/pending_orders", response_class=HTMLResponse)
async def pending_orders_page(request: Request):
    return templates.TemplateResponse("pending_orders.html", {"request": request})

@app.get("/orders/received_orders", response_class=HTMLResponse)
async def received_orders_page(request: Request):
    return templates.TemplateResponse("received_orders.html", {"request": request})

@app.get("/orders/audit_trail", response_class=HTMLResponse)
async def audit_trail_page(request: Request):
    return templates.TemplateResponse("audit_trail.html", {"request": request})

@app.get("/maintenance", response_class=HTMLResponse)
async def maintenance_page(request: Request):
    return templates.TemplateResponse("maintenance.html", {"request": request})

@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    favicon_path = Path("frontend/static/favicon.ico")
    if not favicon_path.exists():
        return {"error": "Favicon not found"}, 404
    return FileResponse(favicon_path)

# Run server
if __name__ == "__main__":
    import uvicorn
    try:
        logging.info("🚀 Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8004)
    except Exception as e:
        logging.exception("❌ Server failed to start")
        raise