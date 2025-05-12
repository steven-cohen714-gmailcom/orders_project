from fastapi import APIRouter, HTTPException, Request
from backend.utils.send_email import send_email
from weasyprint import HTML
from io import BytesIO
from datetime import datetime
from fastapi.templating import Jinja2Templates
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.post("/email_purchase_order")
async def email_purchase_order(request: Request):
    try:
        # Extract raw HTML from incoming request
        data = await request.json()
        html = data.get("html")
        order_number = data.get("order_number")
        recipient_email = data.get("recipient_email")

        if not html or not order_number or not recipient_email:
            raise HTTPException(status_code=400, detail="Missing required fields: html, order_number, recipient_email")

        logging.info(f"📩 Generating PDF for order {order_number} and sending to {recipient_email}")

        # Generate PDF from raw HTML
        pdf_io = BytesIO()
        HTML(string=html).write_pdf(pdf_io)
        pdf_io.seek(0)
        attachment_bytes = pdf_io.getvalue()

        # Email
        subject = f"Purchase Order {order_number}"
        body = f"Attached is the purchase order {order_number} generated on {datetime.now().strftime('%Y-%m-%d')}."

        await send_email(
            recipient=recipient_email,
            subject=subject,
            body=body,
            attachment_bytes=attachment_bytes,
            attachment_filename=f"order_{order_number}.pdf"
        )

        logging.info(f"✅ Email sent for order {order_number} to {recipient_email}")
        return {"status": "Email sent successfully"}

    except Exception as e:
        logging.exception("❌ Failed to send purchase order email")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
