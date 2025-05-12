from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import io
import os

router = APIRouter()

# Set up template directory
template_path = os.path.join(os.path.dirname(__file__), "../../frontend/templates")
env = Environment(loader=FileSystemLoader(template_path))

@router.post("/preview_pdf_new_order")
async def generate_preview_pdf_for_new_order(request: Request):
    """
    Generate a PDF preview for a new order without saving it to the database.
    The frontend sends raw JSON representing the form data.
    """
    form_data = await request.json()

    template = env.get_template("pdf_template.html")
    html_content = template.render(
        order_number=form_data.get("order_number", "URCxxxx"),
        status="Preview",
        total=form_data.get("total", 0),
        requester_name="PREVIEW ONLY",
        supplier_name="PREVIEW ONLY",
        business_details={
            "company_name": "Universal Recycling",
            "registration_number": "000000",
            "vat_number": "000000",
            "address": "123 Preview Street",
            "phone": "000-000-0000",
            "email": "preview@urc.co.za"
        },
        note_to_supplier=form_data.get("note_to_supplier", ""),
        order_note=form_data.get("order_note", ""),
        items=form_data.get("items", [])
    )

    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)

    return StreamingResponse(pdf_io, media_type="application/pdf", headers={
        "Content-Disposition": "inline; filename=preview_order.pdf"
    })
