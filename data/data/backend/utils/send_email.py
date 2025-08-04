# File: backend/utils/send_email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
import logging
from typing import Optional

load_dotenv()

logging.basicConfig(level=logging.INFO)

async def send_email(
    recipient: str,
    subject: str,
    body: str,
    attachment_bytes: Optional[bytes] = None,
    attachment_filename: Optional[str] = None,
    reply_to_email: Optional[str] = None
):
    try:
        msg = MIMEMultipart()
        sender = os.getenv("EMAIL_FROM") # This should be your system's "from" email
        if not sender:
            raise ValueError("EMAIL_FROM is not defined in .env")

        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        if reply_to_email:
            msg['Reply-To'] = reply_to_email
            logging.info(f"Email Reply-To set to: {reply_to_email}")

        msg.attach(MIMEText(body, 'plain'))

        if attachment_bytes and attachment_filename:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_bytes)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {attachment_filename}")
            msg.attach(part)
        elif attachment_bytes and not attachment_filename:
            logging.warning("Attachment bytes provided but no filename. Attachment will not be sent.")
        
        # MODIFIED: Use generic SMTP variables
        host = os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", 0))
        username = os.getenv("SMTP_USERNAME")
        password = os.getenv("SMTP_PASSWORD")

        if not all([host, port, username, password]):
            raise ValueError("One or more SMTP environment variables are missing (SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)")

        with smtplib.SMTP(host, port) as server:
            server.starttls() # Use starttls for port 587
            # If using port 465 (SSL), you might use smtplib.SMTP_SSL instead of SMTP and starttls()
            server.login(username, password)
            server.send_message(msg)

        logging.info(f"Email sent to {recipient} with subject '{subject}'")

    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        raise Exception(f"Email sending failed: {str(e)}")
