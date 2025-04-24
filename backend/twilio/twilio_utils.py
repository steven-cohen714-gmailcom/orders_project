import os
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path
import logging
import json

# Set up logging
logging.basicConfig(
    filename="logs/twilio.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
group_members = [
    os.getenv("GROUP_MEMBER_1"),
    os.getenv("GROUP_MEMBER_2"),
    os.getenv("GROUP_MEMBER_3"),
    os.getenv("GROUP_MEMBER_4"),
    os.getenv("GROUP_MEMBER_5"),
    os.getenv("GROUP_MEMBER_6"),
    os.getenv("GROUP_MEMBER_7"),
]

# Initialize Twilio client
client = Client(account_sid, auth_token)

# File to store phone number to most recent order number mapping
PHONE_ORDER_MAPPING_FILE = Path("logs/phone_order_mapping.json")

def save_phone_order_mapping(phone_number: str, order_number: str):
    mapping = {}
    if PHONE_ORDER_MAPPING_FILE.exists():
        with PHONE_ORDER_MAPPING_FILE.open("r", encoding="utf-8") as f:
            mapping = json.load(f)
    mapping[phone_number] = order_number
    with PHONE_ORDER_MAPPING_FILE.open("w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)

def get_order_number_from_phone(phone_number: str) -> str:
    if not PHONE_ORDER_MAPPING_FILE.exists():
        return None
    with PHONE_ORDER_MAPPING_FILE.open("r", encoding="utf-8") as f:
        mapping = json.load(f)
    return mapping.get(phone_number)

def send_whatsapp_notification(order_number: str, total: float):
    message_body = f"New order {order_number} exceeds threshold (R{total:.2f}). Reply 'Authorised' to approve."
    try:
        for member in group_members:
            if member:  # Skip if member is None (not set in .env)
                message = client.messages.create(
                    body=message_body,
                    from_=twilio_number,
                    to=member
                )
                logging.info(f"Sent WhatsApp message to {member} for order {order_number}: {message.sid}")
                # Save the phone number to order number mapping
                save_phone_order_mapping(member, order_number)
        return True
    except Exception as e:
        logging.error(f"Failed to send WhatsApp notification for order {order_number}: {str(e)}")
        return False