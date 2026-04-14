#!/usr/bin/env python3
import base64
import os

# Read the logo file and convert to base64
logo_path = '/home/steven_cohen714/orders_project/frontend/static/images/universal_logo.jpg'
with open(logo_path, 'rb') as f:
    logo_data = base64.b64encode(f.read()).decode()

logo_base64 = f"data:image/jpeg;base64,{logo_data}"

# Read the current email engine
with open('/home/steven_cohen714/orders_project/backend/utils/email_and_alerts_engine.py', 'r') as f:
    content = f.read()

# Find and replace the _build_supplier_email function
old_function_start = "def _build_supplier_email(details: dict) -> Tuple[str, str]:"
new_function = '''def _build_supplier_email(details: dict) -> Tuple[str, str, str]:
    """
    Build professional supplier notification email with HTML and logo.
    Returns (subject, plain_body, html_body)
    """
    # Format contact name
    contact = details['supplier_contact'] or "Procurement Team"

    # Format date (extract date from ISO timestamp)
    order_date = details['created_date'][:10] if details['created_date'] else now_utc_iso()[:10]

    # Build items table (plain text)
    items_text = "\\n"
    for item in details['items']:
        item_code = item['item_code'] or ''
        desc = item['item_description'] or ''
        qty = float(item['qty_ordered'] or 0)
        price = float(item['price'] or 0)
        total = float(item['total'] or 0)
        items_text += f"  • {item_code} - {desc}\\n"
        items_text += f"    Quantity: {qty:,.2f} | Unit Price: R{price:,.2f} | Total: R{total:,.2f}\\n"

    # Build items table (HTML)
    items_html = ""
    for item in details['items']:
        item_code = item['item_code'] or ''
        desc = item['item_description'] or ''
        qty = float(item['qty_ordered'] or 0)
        price = float(item['price'] or 0)
        total = float(item['total'] or 0)
        items_html += f"""
        <tr>
            <td>{item_code}</td>
            <td>{desc}</td>
            <td style="text-align: right;">{qty:,.2f}</td>
            <td style="text-align: right;">R{price:,.2f}</td>
            <td style="text-align: right;">R{total:,.2f}</td>
        </tr>"""

    # Build subject
    subject = f"New Purchase Order #{details['order_number']} from {details['company_name']}"

    # Build plain text body
    plain_body = f"""Dear {contact},

This email confirms the placement of a new Purchase Order (#{details['order_number']}) by {details['company_name']} for the supply of goods/services.

Please review the order details below carefully, which include the items, quantities, agreed prices, and delivery information.

ORDER DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PO Number:          {details['order_number']}
Order Date:         {order_date}
Total Value:        R{details['total']:,.2f}
Payment Terms:      {details['payment_terms']}

DELIVERY ADDRESS:
{details['company_address']}

ITEMS ORDERED:
{items_text}
"""

    # Add note to supplier if present (plain text)
    if details['note_to_supplier']:
        plain_body += f"""
SPECIAL INSTRUCTIONS:
{details['note_to_supplier']}
"""

    plain_body += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:

1. CONFIRMATION: Please acknowledge receipt of this Purchase Order and confirm your acceptance of the terms by replying to this email within 2 business days.

2. PROCESSING: Please proceed with the fulfillment of the order as per the specifications listed above.

3. INVOICING: Reference the Purchase Order number #{details['order_number']} on all corresponding invoices and shipping documents.

If you have any questions regarding this order, please contact our Procurement Department at {details['company_telephone']} or reply to this email.

Thank you for your prompt attention.

Sincerely,

Procurement Department
{details['company_name']}
{details['company_telephone']}
"""

    # Build HTML body with logo
    logo_base64 = "''' + logo_base64 + '''"

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-bottom: 3px solid #007bff; }}
        .logo {{ width: 140px; margin-bottom: 10px; }}
        h1 {{ color: #007bff; margin: 10px 0; font-size: 24px; }}
        .info-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .info-table th {{ background-color: #007bff; color: white; padding: 12px; text-align: left; }}
        .info-table td {{ padding: 10px; border: 1px solid #ddd; }}
        .items-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .items-table th {{ background-color: #007bff; color: white; padding: 10px; text-align: left; }}
        .items-table td {{ padding: 8px; border: 1px solid #ddd; }}
        .note-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        .steps {{ background-color: #e7f3ff; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .steps h3 {{ color: #007bff; margin-top: 0; }}
        .steps ol {{ margin: 10px 0; padding-left: 20px; }}
        .steps li {{ margin: 8px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="{logo_base64}" alt="Universal Recycling Company Logo" class="logo">
            <h1>Purchase Order #{details['order_number']}</h1>
            <p style="margin: 5px 0;"><strong>{details['company_name']}</strong></p>
            <p style="margin: 5px 0;">{details['company_address']}</p>
            <p style="margin: 5px 0;">Tel: {details['company_telephone']}</p>
        </div>

        <p>Dear {contact},</p>

        <p>This email confirms the placement of a new <strong>Purchase Order (#{details['order_number']})</strong> by {details['company_name']} for the supply of goods/services.</p>

        <p>Please review the order details below carefully, which include the items, quantities, agreed prices, and delivery information.</p>

        <table class="info-table">
            <tr>
                <th>PO Number</th>
                <td>{details['order_number']}</td>
            </tr>
            <tr>
                <th>Order Date</th>
                <td>{order_date}</td>
            </tr>
            <tr>
                <th>Total Value</th>
                <td><strong>R{details['total']:,.2f}</strong></td>
            </tr>
            <tr>
                <th>Payment Terms</th>
                <td>{details['payment_terms']}</td>
            </tr>
            <tr>
                <th>Delivery Address</th>
                <td>{details['company_address']}</td>
            </tr>
        </table>

        <h2 style="color: #007bff;">Items Ordered</h2>
        <table class="items-table">
            <thead>
                <tr>
                    <th>Item Code</th>
                    <th>Description</th>
                    <th style="text-align: right;">Quantity</th>
                    <th style="text-align: right;">Unit Price</th>
                    <th style="text-align: right;">Total</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
"""

    # Add note to supplier if present (HTML)
    if details['note_to_supplier']:
        html_body += f"""
        <div class="note-box">
            <h3 style="margin-top: 0; color: #856404;">⚠️ Special Instructions</h3>
            <p style="margin: 0;">{details['note_to_supplier'].replace(chr(10), '<br>')}</p>
        </div>
"""

    html_body += f"""
        <div class="steps">
            <h3>Next Steps</h3>
            <ol>
                <li><strong>CONFIRMATION:</strong> Please acknowledge receipt of this Purchase Order and confirm your acceptance of the terms by replying to this email within 2 business days.</li>
                <li><strong>PROCESSING:</strong> Please proceed with the fulfillment of the order as per the specifications listed above.</li>
                <li><strong>INVOICING:</strong> Reference the Purchase Order number <strong>#{details['order_number']}</strong> on all corresponding invoices and shipping documents.</li>
            </ol>
        </div>

        <p>If you have any questions regarding this order, please contact our Procurement Department at <strong>{details['company_telephone']}</strong> or reply to this email.</p>

        <p>Thank you for your prompt attention.</p>

        <div class="footer">
            <p><strong>Sincerely,</strong></p>
            <p>Procurement Department<br>
            {details['company_name']}<br>
            {details['company_telephone']}</p>
        </div>
    </div>
</body>
</html>
"""

    return subject, plain_body, html_body'''

# Find the start of the old function
start_pos = content.find(old_function_start)
if start_pos == -1:
    print("ERROR: Could not find _build_supplier_email function")
    exit(1)

# Find the end of the old function (next "def " at the same indentation level)
search_from = start_pos + len(old_function_start)
next_def = content.find("\\ndef send_supplier_notification(", search_from)
if next_def == -1:
    print("ERROR: Could not find end of _build_supplier_email function")
    exit(1)

# Replace the old function
new_content = content[:start_pos] + new_function + content[next_def:]

# Now update the send_supplier_notification function to use HTML
old_call = "subject, body = _build_supplier_email(details)"
new_call = "subject, plain_body, html_body = _build_supplier_email(details)"
new_content = new_content.replace(old_call, new_call)

old_transport = "_call_transport(send_fn, [supplier_email], subject, body)"
new_transport = "send_fn([supplier_email], subject, plain_body, html_body)"
new_content = new_content.replace(old_transport, new_transport)

# Write the updated content
with open('/home/steven_cohen714/orders_project/backend/utils/email_and_alerts_engine.py', 'w') as f:
    f.write(new_content)

print("✅ Email engine updated with HTML support and logo embedding")
print(f"   Logo embedded as base64 (size: {len(logo_data)} bytes)")
