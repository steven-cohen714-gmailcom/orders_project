from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os
import io
import logging
from backend.database import get_db_connection

router = APIRouter()

@router.get("/generate_pdf_for_order/{order_id}")
async def generate_pdf_for_order(order_id: int):
    try:
        template_path = os.path.join(os.path.dirname(__file__), "../../frontend/templates")
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("pdf_template.html")

        with get_db_connection() as conn:
            conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
            cursor = conn.cursor()

            cursor.execute("""
                SELECT o.*, s.name AS supplier, r.name AS requester
                FROM orders o
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()

            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            items = cursor.fetchall()

            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            business_details = cursor.fetchone()
            if not business_details:
                raise HTTPException(status_code=404, detail="Business details not found")

        logo_path = "file:///Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/images/universal_logo.jpg"
        html = template.render(
            order=order,
            items=items,
            business_details=business_details,
            logo_path=logo_path,
            note_to_supplier=order.get("note_to_supplier", "")
        )

        pdf_io = io.BytesIO()
        HTML(string=html).write_pdf(pdf_io)
        pdf_io.seek(0)

        return StreamingResponse(pdf_io, media_type="application/pdf", headers={
            "Content-Disposition": f"inline; filename=order_{order_id}.pdf"
        })

    except Exception as e:
        logging.exception(f"PDF generation failed for order {order_id}")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
