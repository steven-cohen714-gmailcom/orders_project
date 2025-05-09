import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

async def send_email(recipient: str, subject: str, body: str, attachment_path: str = None):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_FROM")
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(attachment_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}"
            )
            
            msg.attach(part)

        with smtplib.SMTP(os.getenv("MAILTRAP_HOST"), os.getenv("MAILTRAP_PORT")) as server:
            server.starttls()
            server.login(os.getenv("MAILTRAP_USERNAME"), os.getenv("MAILTRAP_PASSWORD"))
            server.send_message(msg)
            
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")