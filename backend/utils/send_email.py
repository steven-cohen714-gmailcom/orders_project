import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

async def send_email(recipient: str, subject: str, body: str, attachment_path: str = None):
    try:
        msg = MIMEMultipart()
        sender = os.getenv("EMAIL_FROM")
        if not sender:
            raise ValueError("EMAIL_FROM is not defined in .env")

        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            if not os.path.exists(attachment_path):
                raise FileNotFoundError(f"Attachment not found: {attachment_path}")
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            msg.attach(part)

        host = os.getenv("MAILTRAP_HOST")
        port = int(os.getenv("MAILTRAP_PORT", 0))
        username = os.getenv("MAILTRAP_USERNAME")
        password = os.getenv("MAILTRAP_PASSWORD")

        if not all([host, port, username, password]):
            raise ValueError("One or more Mailtrap environment variables are missing")

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)

        logging.info(f"Email sent to {recipient} with subject '{subject}'")

    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        raise Exception(f"Email sending failed: {str(e)}")
