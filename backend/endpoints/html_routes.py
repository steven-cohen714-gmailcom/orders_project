from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.database import get_db_connection
import logging

# Logging setup
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/orders/new", response_class=HTMLResponse)
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
            business_details = dict(row) if row else {
                "company_name": "Universal Recycling Company Pty Ltd",
                "address_line1": "123 Industrial Road",
                "address_line2": "Unit 4",
                "city": "Cape Town",
                "province": "Western Cape",
                "postal_code": "8001",
                "telephone": "+27 21 555 1234",
                "vat_number": "VAT123456789"
            }
            logging.info(f"Business details fetched: {business_details}")

        return templates.TemplateResponse(
            "new_order.html",
            {
                "request": request,
                "requesters": requesters,
                "suppliers": suppliers,
                "items": items,
                "projects": projects,
                "business_details": business_details
            }
        )
    except Exception as e:
        logging.error(f"Error rendering new order page: {str(e)}")
        raise

@router.get("/orders/pending_orders", response_class=HTMLResponse)
async def pending_orders_page(request: Request):
    try:
        return templates.TemplateResponse(
            "pending_orders.html",
            {"request": request}
        )
    except Exception as e:
        logging.error(f"Error rendering pending orders page: {str(e)}")
        raise