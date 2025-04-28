from twilio.rest import Client
import os
from pathlib import Path
import json

# Twilio credentials from environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Load group members from environment variables
group_members = [
    os.getenv(f"GROUP_MEMBER_{i}") for i in range(1, 8)
    if os.getenv(f"GROUP_MEMBER_{i}")
]

async def send_whatsapp_message(order_number: str, message_body: str):
    """
    Send a WhatsApp message to group members for order authorization.
    
    Args:
        order_number (str): The order number associated with the message.
        message_body (str): The message to send.
    """
    # Log the message SID mapping
    mapping_path = Path("logs/message_sid_mapping.json")
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    if mapping_path.exists():
        with mapping_path.open("r", encoding="utf-8") as f:
            message_mapping = json.load(f)
    else:
        message_mapping = {}

    for member in group_members:
        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_phone,
                to=member
            )
            message_mapping[message.sid] = order_number
        except Exception as e:
            with open("logs/twilio.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] Failed to send WhatsApp message to {member}: {str(e)}\n")

    # Save the updated message SID mapping
    with mapping_path.open("w", encoding="utf-8") as f:
        json.dump(message_mapping, f, indent=2)
