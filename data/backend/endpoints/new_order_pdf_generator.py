# File: backend/endpoints/new_order_pdf_generator.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import io
import os
import logging
from backend.database import get_db_connection  # ✅ Pulls live business details from DB

router = APIRouter()

# ✅ Relative paths for portability
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../../frontend/templates")
LOGO_PATH = "file://" + os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../frontend/static/images/universal_logo.jpg")
)
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))


@router.post("/preview_pdf_new_order")
async def generate_preview_pdf_for_new_order(request: Request):
    try:
        form_data = await request.json()

        # ✅ Enforce required fields
        required_fields = ["order_number", "created_date", "supplier_name", "requester_name", "items"]
        missing = [field for field in required_fields if field not in form_data or form_data[field] is None]
        if missing:
            raise HTTPException(status_code=422, detail=f"Missing required fields: {', '.join(missing)}")

        # ✅ Use DB-sourced business details — not hardcoded
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            business_details = cursor.fetchone()
            if not business_details:
                raise HTTPException(status_code=404, detail="Business details not found")

        # ✅ Sanitize and prepare order
        order = {
            "order_number": form_data["order_number"],
            "status": form_data.get("status", "Pending"),
            "created_date": form_data["created_date"],
            "supplier": form_data["supplier_name"],
            "requester": form_data["requester_name"],
            "order_note": form_data.get("order_note", ""),
            "note_to_supplier": form_data.get("note_to_supplier", ""),
            "total": form_data.get("total", 0)
        }

        # ✅ Compute item-level totals safely
        items = form_data.get("items", [])
        for item in items:
            try:
                qty = float(item.get("qty_ordered", 0))
                price = float(item.get("price", 0))
                item["total"] = qty * price
            except Exception:
                item["total"] = 0.0

        html_content = env.get_template("pdf_template.html").render(
            order=order,
            items=items,
            business_details=business_details,
            logo_path=LOGO_PATH
        )

        pdf_io = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_io)
        pdf_io.seek(0)

        return StreamingResponse(pdf_io, media_type="application/pdf", headers={
            "Content-Disposition": "inline; filename=preview_order.pdf"
        })

    except Exception as e:
        logging.exception("Preview PDF generation failed")
        raise HTTPException(status_code=500, detail=f"Failed to generate preview PDF: {str(e)}")
