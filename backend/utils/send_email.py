import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # ✅ Load environment variables from .env

def send_purchase_order_email(to_address, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "tintin@urc.co.za"
    msg["To"] = to_address
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(attachment_path)
            )

    smtp_host = os.getenv("MAILTRAP_HOST")
    smtp_port = int(os.getenv("MAILTRAP_PORT", 2525))
    smtp_user = os.getenv("MAILTRAP_USER")
    smtp_pass = os.getenv("MAILTRAP_PASS")

    try:
        print(f"📡 Connecting to {smtp_host}:{smtp_port} with user {smtp_user}")
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.set_debuglevel(1)  # Debug output
            server.ehlo()
            server.starttls()  # Always use TLS
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        raise Exception(f"Email send failed: {e}")
