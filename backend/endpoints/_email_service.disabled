# File: backend/endpoints/email_service.py

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from io import BytesIO
import base64
import logging
import os  # For os.getenv
from datetime import datetime

from backend.utils.send_email import send_email
from backend.database import get_db_connection
from backend.utils.permissions_utils import require_login

router = APIRouter(tags=["email"])

# Pydantic model for the incoming email request payload
class SendPdfEmailPayload(BaseModel):
    pdf_base64: str                # The PDF content as a Base64 string
    order_number: str             # The order number (available for new and existing orders)
    recipient_email: EmailStr     # The email address to send to (always provided by frontend)
    order_id: Optional[int] = None # Optional: present for existing orders, None for new previews
    save_email_to_supplier: Optional[bool] = False # Optional: if true, save recipient_email to supplier record

@router.post("/email/send_pdf", dependencies=[Depends(require_login)])
async def send_pdf_email(request: Request, payload: SendPdfEmailPayload):
    try:
        current_user = request.session.get("user")
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        user_id = current_user["id"]
        username = current_user["username"]

        # Decode the Base64 PDF content
        pdf_bytes = base64.b64decode(payload.pdf_base64)
        attachment_filename = f"Purchase_Order_{payload.order_number}.pdf"

        # Determine Aaron's email for reply-to
        aaron_email = os.getenv("AARON_EMAIL")
        if not aaron_email:
            logging.warning("AARON_EMAIL not set in .env. Reply-To header will not be set.")
            aaron_email = None

        logging.info(f"📩 Attempting to send PDF for order {payload.order_number} to {payload.recipient_email}")

        # Send the email
        subject = f"Purchase Order {payload.order_number} from Universal Recycling"
        body = f"Dear Supplier,\n\nPlease find attached Purchase Order {payload.order_number}.\n\nKind regards,\nUniversal Recycling"

        await send_email(
            recipient=payload.recipient_email,
            subject=subject,
            body=body,
            attachment_bytes=pdf_bytes,
            attachment_filename=attachment_filename,
            reply_to_email=aaron_email
        )

        # Handle Audit Trail / Order Note update
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if payload.order_id:
                # For existing orders, log to audit_trail table
                details = f"Purchase order {payload.order_number} emailed to {payload.recipient_email} by {username}"
                cursor.execute(
                    """
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (payload.order_id, "Email Sent", details, datetime.now().isoformat(), user_id)
                )
            else:
                # For new orders (previews), return a flag to frontend to update order_note
                logging.info(f"Email sent for new order preview {payload.order_number}. Frontend needs to update order_note.")
                return {"message": f"Purchase Order {payload.order_number} emailed successfully", "update_order_note": True}
            
            # Optional: Save manual email to supplier if flag is set and order_id is available
            if payload.save_email_to_supplier and payload.order_id:
                cursor.execute("SELECT supplier_id FROM orders WHERE id = ?", (payload.order_id,))
                order_supplier_id = cursor.fetchone()
                if order_supplier_id and order_supplier_id["supplier_id"]:
                    cursor.execute("UPDATE suppliers SET email = ? WHERE id = ?", 
                                   (payload.recipient_email, order_supplier_id["supplier_id"]))
                    logging.info(f"Manually provided email '{payload.recipient_email}' saved to supplier ID {order_supplier_id['supplier_id']}.")
                else:
                    logging.warning(f"Could not save email to supplier for order {payload.order_id}: Supplier ID not found.")

            conn.commit()

        logging.info(f"✅ Email sent for order {payload.order_number} to {payload.recipient_email} and logged to audit trail.")
        return {"message": f"Purchase Order {payload.order_number} emailed successfully"}

    except HTTPException as he:
        logging.warning(f"Email PO HTTP error: {he.detail}")
        raise he
    except Exception as e:
        logging.exception("❌ Failed to send purchase order email via new service")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")