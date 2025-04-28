from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from backend.twilio.twilio_utils import send_whatsapp_message
from backend.database import get_db_connection
import logging
import json
from pathlib import Path

# Logging setup
logging.basicConfig(
    filename="logs/whatsapp_log.txt",
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
)

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

class WhatsAppMessage(BaseModel):
    order_number: str
    message: str
    to_number: str

@router.post("/send")
async def send_whatsapp(msg: WhatsAppMessage):
    try:
        sid = send_whatsapp_message(
            to_number=msg.to_number,
            message=f"Purchase Order {msg.order_number}: {msg.message}",
        )
        # Log message SID mapping
        mapping_file = Path("logs/message_sid_mapping.json")
        mapping = {}
        if mapping_file.exists():
            with open(mapping_file, "r") as f:
                mapping = json.load(f)
        mapping[sid] = {"order_number": msg.order_number, "to_number": msg.to_number}
        with open(mapping_file, "w") as f:
            json.dump(mapping, f, indent=2)
        logging.info(
            json.dumps(
                {
                    "action": "sent_message",
                    "order_number": msg.order_number,
                    "to": msg.to_number,
                    "message_sid": sid,
                }
            )
        )
        return {"status": "Message sent", "sid": sid}
    except Exception as e:
        logging.error(json.dumps({"error": str(e), "type": "send"}))
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        from_number = form_data.get("From", "")
        message = form_data.get("Body", "").lower().strip()
        message_sid = form_data.get("MessageSid", "")

        logging.info(
            json.dumps(
                {
                    "action": "received_message",
                    "from": from_number,
                    "message": message,
                    "message_sid": message_sid,
                }
            )
        )

        # Load message SID mapping
        mapping_file = Path("logs/message_sid_mapping.json")
        mapping = {}
        if mapping_file.exists():
            with open(mapping_file, "r") as f:
                mapping = json.load(f)

        order_info = mapping.get(message_sid)
        if not order_info:
            logging.error(
                json.dumps({"error": f"No order found for message SID {message_sid}"})
            )
            return {"status": "No order found"}

        order_number = order_info["order_number"]

        if "authorised" in message:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE orders SET status = 'Authorised' WHERE order_number = ?",
                    (order_number,)
                )
                cursor.execute(
                    """
                    INSERT INTO audit_trail (order_id, action, details, user_id)
                    VALUES ((SELECT id FROM orders WHERE order_number = ?), 'Authorised', ?, 0)
                    """,
                    (order_number, f"Order authorised via WhatsApp from {from_number}"),
                )
                conn.commit()

            logging.info(
                json.dumps(
                    {
                        "action": "order_authorised",
                        "order_number": order_number,
                        "from": from_number,
                    }
                )
            )
            return {"status": "Order authorised"}
        else:
            return {"status": "Message received"}
    except Exception as e:
        logging.error(json.dumps({"error": str(e), "type": "webhook"}))
        return {"status": "Error processing webhook"}