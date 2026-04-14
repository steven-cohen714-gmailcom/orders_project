# File: backend/endpoints/email.py
# NOTE: This module is the ONLY allowed direct use of send_email().
# Reason: supplier PDF attachments. All other emails must go through
# backend/utils/email_and_alerts_engine.dispatch(...)

from __future__ import annotations

import base64
import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from backend.database import get_db_connection
from backend.utils.send_email import send_email

from backend.utils.permissions_utils import require_login

router = APIRouter(prefix="/email", tags=["email"])

class EmailSendRequest(BaseModel):
    recipient_email: EmailStr
    order_id: Optional[int] = None
    order_number: Optional[str] = None
    pdf_base64: str
    save_email_to_supplier: bool = False  # matches frontend payload

@router.post("/send_pdf")
async def send_pdf_email(payload: EmailSendRequest, user: dict = Depends(require_login)):
    """
    Accepts a base64 PDF from the front-end and emails it to the supplier.
    - From address is forced by EMAIL_FROM in .env (aaron@urc.co.za).
    - Reply-To/BCC come from .env if set.
    - Optionally stores supplier email for this order when save_email=True.
    - Always logs to audit_trail if order_id is supplied.
    """
    # 1) Decode the PDF (supports raw base64 or data URLs like "data:application/pdf;base64,AAA...")
    try:
        b64 = payload.pdf_base64.split(",", 1)[-1].strip()
        pdf_bytes = base64.b64decode(b64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 PDF")

    # 2) Subject/body/filename
    po_num = payload.order_number or "PurchaseOrder"
    subject = f"Universal Recycling Purchase Order {po_num}"
    body = (
        f"Dear Supplier,\n\n"
        f"Please find attached Purchase Order {po_num}.\n\n"
        f"Kind regards,\n"
        f"Universal Recycling System"
    )
    filename = f"{po_num}.pdf".replace(" ", "_")

    # 3) Send the email (this will auto-BCC and enforce From per send_email.py)
    try:
        await send_email(
            recipient=payload.recipient_email,
            subject=subject,
            body=body,
            attachment_bytes=pdf_bytes,
            attachment_filename=filename,
        )
    except Exception as e:
        # Bubble up with a clean message; full details are already logged in send_email.py
        raise HTTPException(status_code=502, detail=f"SMTP send failed: {e}")

    # 4) Optional: store supplier email + audit trail
    if payload.order_id:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Audit trail
            cur.execute(
                "INSERT INTO audit_trail (order_id, action, details, user_id, action_date) "
                "VALUES (?, 'Emailed', ?, ?, datetime('now'))",
                (
                    payload.order_id,
                    f"Emailed PO {po_num} to {payload.recipient_email}",
                    user.get("id"),
                ),
            )

            # Save supplier email if asked and the order has a supplier_id
            if payload.save_email_to_supplier:
                cur.execute("SELECT supplier_id FROM orders WHERE id = ?", (payload.order_id,))
                row = cur.fetchone()
                if row and row[0]:
                    cur.execute(
                        "UPDATE suppliers SET email = ? WHERE id = ? AND (email IS NULL OR email = '')",
                        (payload.recipient_email, row[0]),
                    )

            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            # Don’t fail the whole request just because audit/save failed
            # but do return a flag so the UI could inform if needed.
            return {
                "success": True,
                "message": "Email sent, but audit/save failed.",
                "update_order_note": bool(payload.order_number and payload.order_number.strip()),
                "db_warning": str(e),
            }
        finally:
            conn.close()

    # 5) Success
    return {
        "success": True,
        "message": "Email sent.",
        # For previews/new orders the front-end may want to stamp the note
        "update_order_note": bool(payload.order_number and payload.order_number.strip()),
    }
