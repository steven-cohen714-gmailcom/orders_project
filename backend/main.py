from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from backend.endpoints.lookups import router as lookups_router
from backend.endpoints.orders import router as orders_router
from backend.database import init_db
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
app.include_router(orders_router, prefix="/orders")

# HTML routes using Jinja2 templates
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request):
    return templates.TemplateResponse("new_order.html", {
        "request": request,
        "requesters": [],  # Add actual data if needed
        "suppliers": [],   # Add actual data if needed
        "business_details": {
            "company_name": "Universal Recycling Company Pty Ltd",
            "address_line1": "123 Industrial Road",
            "address_line2": "Unit 4",
            "city": "Cape Town",
            "province": "Western Cape",
            "postal_code": "8001",
            "telephone": "+27 21 555 1234",
            "vat_number": "VAT123456789"
        }
    })

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