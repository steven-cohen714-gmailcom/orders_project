from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from backend.utils.send_email import send_purchase_order_email
from weasyprint import HTML
from io import BytesIO
import logging
import httpx
import os
from datetime import datetime

router = APIRouter()

@router.post("/email_purchase_order")
async def email_purchase_order(request: Request):
    try:
        data = await request.json()
        html = data.get("html")
        order_id = data.get("order_id")

        if not html and not order_id:
            raise HTTPException(status_code=400, detail="Missing HTML or order_id")

        # 🧠 If HTML not sent, fetch it from dedicated HTML endpoint
        if not html and order_id:
            async with httpx.AsyncClient() as client:
                html_url = f"http://localhost:8004/orders/api/html_for_order/{order_id}"
                html_response = await client.get(html_url)
                if html_response.status_code != 200:
                    raise HTTPException(status_code=500, detail=f"Could not retrieve HTML for order {order_id}")
                html = html_response.text

        # 🧱 Generate PDF from HTML
        pdf_io = BytesIO()
        HTML(string=html).write_pdf(target=pdf_io)
        pdf_bytes = pdf_io.getvalue()

        # 📨 Save temp PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"order_email_{timestamp}.pdf"
        filepath = f"/Users/stevencohen/Projects/universal_recycling/orders_project/tmp/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(pdf_bytes)

        # 📬 Send Email
        send_purchase_order_email(
            to_address="tintin@urc.co.za",
            subject="Purchase Order",
            body="Please find the attached Purchase Order.",
            attachment_path=filepath
        )

        return JSONResponse(content={"detail": "✅ Email sent successfully"}, status_code=200)

    except Exception as e:
        logging.exception("Email send failed")
        raise HTTPException(status_code=500, detail=f"Email send failed: {e}")
