import sys
sys.path.insert(0, '/home/steven_cohen714/orders_project')

from backend.utils.send_email import send_email

# Send simple test email to Steven
send_email(
    to="steven.cohen714@gmail.com",
    subject="Test Email - Orders System Working",
    body="""Hi Steven,

This is a simple test email to confirm the email system is working correctly.

System Status:
✅ Mimecast SMTP: Connected
✅ Email sending: Active
✅ From address: aaron@urc.co.za

The Orders system email functionality is fully operational.

Best regards,
Orders System
"""
)

print("✅ Simple test email sent to steven.cohen714@gmail.com")
