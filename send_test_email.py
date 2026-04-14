import sys
sys.path.insert(0, '/home/steven_cohen714/orders_project')

from backend.utils.send_email import send_email

# Send test email to Steven
send_email(
    to="steven.cohen714@gmail.com",
    subject="Email System is LIVE! 🎉",
    body="""Hi Steven,

Success! The email system is now working via Mimecast SMTP.

Configuration:
- SMTP Server: za-smtp-outbound-1.mimecast.co.za
- Port: 587
- From: aaron@urc.co.za
- Authentication: Working

The Orders system can now send customer emails!

Best regards,
Orders System
"""
)

print("✅ Email sent to steven.cohen714@gmail.com")
