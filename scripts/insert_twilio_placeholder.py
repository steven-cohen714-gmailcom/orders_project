from pathlib import Path

orders_path = Path("backend/endpoints/orders.py")
code = orders_path.read_text()

marker = "status = determine_status(total, auth_threshold)"
block = '''status = determine_status(total, auth_threshold)

        if total > auth_threshold:
            # 🔔 Placeholder: Send Twilio WhatsApp notification to authorisers
            # from ..integrations.whatsapp import notify_authorisers
            # notify_authorisers(order_number=order.order_number, amount=total)
            print(f"[WHATSAPP] Order {order.order_number} exceeds threshold, notify for auth.")'''

if marker in code:
    updated = code.replace(marker, block)
    orders_path.write_text(updated)
    print("✅ Twilio placeholder injected.")
else:
    print("❌ Could not find injection marker. No changes made.")
