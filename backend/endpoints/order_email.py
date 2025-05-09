from fastapi import APIRouter, HTTPException
import os
from backend.utils.send_email import send_email
from datetime import datetime
from backend.database import get_db_connection

router = APIRouter()

@router.post("/email_purchase_order/{order_id}")
async def email_purchase_order(order_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_number, s.email
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            order_number, recipient_email = order

        if not recipient_email:
            raise HTTPException(status_code=400, detail="Supplier email not provided")

        subject = f"Purchase Order {order_number}"
        body = f"Attached is the purchase order {order_number} generated on {datetime.now().strftime('%Y-%m-%d')}"
        attachment_path = f"data/pdfs/order_{order_number}.pdf"
        
        if not os.path.exists(attachment_path):
            raise HTTPException(status_code=404, detail="PDF not found")
        
        await send_email(
            recipient=recipient_email,
            subject=subject,
            body=body,
            attachment_path=attachment_path
        )
        return {"status": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")