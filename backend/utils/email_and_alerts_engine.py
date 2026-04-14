# backend/utils/email_and_alerts_engine.py
"""
Lean email/alerts engine (shim).
- Reviewer alert on creation/draft submit: implemented here (small, testable).
- All other legacy triggers: forwarded to email_and_alerts_engine_old.py (while we migrate).
- Writes clear logs:
    logs/email_dispatch_log.txt
    logs/authorisations_log.txt
"""

from __future__ import annotations

import os
import sqlite3
from typing import Iterable, List, Optional, Tuple, Any

from backend.database import get_db_connection
from backend.utils.time_utils import now_utc_iso

# --------------------------
# Logging (engine-level)
# --------------------------
from backend.utils.logging_utils import get_logger
_email_log = get_logger("email_dispatch")
_authz_log = get_logger("authorisations")

_email_log.info("🔧 email/alerts shim loaded")

# In-process idempotency (avoid duplicate sends in one run)
_SENT = set()

# --------------------------
# Transport (tolerant import)
# --------------------------
def _get_transport():
    """
    Expect backend/utils/send_email.py to expose send_email.
    We only call (to_list, subject, body) or keyword equivalent.
    """
    try:
        from .send_email import send_email as _send  # type: ignore
        return _send
    except Exception as e:
        _email_log.error(f"❌ email transport import failed: {e}")
        return None

def _call_transport(send_fn, to: List[str], subject: str, body: str):
    try:
        return send_fn(to, subject, body)
    except TypeError:
        try:
            return send_fn(to=to, subject=subject, body=body)
        except TypeError:
            # Some transports only accept single recipient → fan out
            results = []
            for addr in to:
                results.append(send_fn([addr], subject, body))
            return results

# --------------------------
# Minimal data lookups
# --------------------------
def _get_order_header(order_id: int) -> Tuple[str, Optional[str], float, Optional[str]]:
    """
    (order_number, supplier_name, total, created_date)
    """
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT o.order_number,
                   o.total,
                   o.created_date,
                   s.name AS supplier_name
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            WHERE o.id = ?
        """, (order_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Order {order_id} not found")
        return (
            row["order_number"],
            row["supplier_name"],
            float(row["total"] or 0.0),
            row["created_date"],
        )

def _get_review_recipients() -> List[str]:
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT TRIM(COALESCE(email,'')) AS email
            FROM users
            WHERE can_receive_review_notifications = 1
        """)
        emails = [r["email"] for r in cur.fetchall() if r["email"]]
        # dedupe
        seen = set(); out = []
        for e in emails:
            if e not in seen:
                out.append(e); seen.add(e)
        return out

# --------------------------
# Content
# --------------------------
def _base_url() -> str:
    return (os.getenv("FRONTEND_BASE_URL") or os.getenv("APP_BASE_URL") or "http://localhost:8004").rstrip("/")

def _build_reviewer_email(order_number: str,
                          supplier_name: Optional[str],
                          total: float) -> Tuple[str, str]:
    sup = supplier_name or "(unknown supplier)"
    tot = f"R{total:,.2f}"
    subject = f"Review order {order_number}"
    body = (
        f"A new order {order_number} is ready for review.\n"
        f"Supplier: {sup}\n"
        f"Total: {tot}\n\n"
        f"Open the Review queue:\n{_base_url()}/orders/review_orders\n\n"
        f"— Universal Recycling System"
    )
    return subject, body

def _get_authorisers_for_band(required_band: Optional[int]) -> List[str]:
    """
    Emails of users allowed to authorise for this band (>= required_band).
    Detects band column robustly; falls back to none if not found.
    """
    if required_band is None:
        return []
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(users)")
        cols = {r["name"].lower() for r in cur.fetchall()}

        # pick whichever band column exists
        band_col = None
        for c in ("auth_threshold_band", "threshold_band", "authorisation_band", "auth_band"):
            if c in cols:
                band_col = c
                break
        if not band_col:
            _email_log.warning("AUTHORISER_NOTIF: no band column on users table")
            return []

        active_filter = "AND active = 1" if "active" in cols else ""
        cur.execute(
            f"""
            SELECT TRIM(COALESCE(email,'')) AS email
            FROM users
            WHERE email IS NOT NULL AND email <> ''
              AND {band_col} IS NOT NULL
              AND CAST({band_col} AS INTEGER) >= CAST(? AS INTEGER)
              {active_filter}
            ORDER BY CAST({band_col} AS INTEGER) DESC, id ASC
            """,
            (required_band,),
        )
        # dedupe
        seen, out = set(), []
        for r in cur.fetchall():
            e = r["email"]
            if e and e not in seen:
                out.append(e); seen.add(e)
        return out

def _send_authoriser_notif(order_id: int, required_band: Optional[int], total_hint: Optional[float]) -> bool:
    """
    Minimal email to authorisers for the given band.
    """
    if required_band is None:
        _email_log.warning(f"AUTHORISER_NOTIF: required_band missing for order_id={order_id}")
        return False
    try:
        order_number, _supplier_name, total, _created_date = _get_order_header(order_id)
        if total_hint is not None:
            try:
                total = float(total_hint)
            except Exception:
                pass
    except Exception as e:
        _email_log.error(f"AUTHORISER_NOTIF: load order header failed order_id={order_id}: {e}")
        return False

    recipients = _get_authorisers_for_band(int(required_band))
    if not recipients:
        _email_log.info(f"AUTHORISER_NOTIF: no recipients for band={required_band} order_id={order_id}")
        return False

    subject = f"Order {order_number} requires Band {required_band} authorisation"
    body = (
        f"Dear Approver,\n\n"
        f"Order {order_number} requires Band {required_band} authorisation.\n"
        f"Total: R{float(total):,.2f}\n\n"
        f"Review & authorise here:\n{_base_url()}/orders/authorisations\n\n"
        f"— Universal Recycling System"
    )

    # Preview
    try:
        _email_log.info(
            "📧 EMAIL PREVIEW | to=%s | subject=%s\n---BODY START---\n%s\n---BODY END---",
            recipients, subject, body
        )
    except Exception:
        pass

    send_fn = _get_transport()
    if not send_fn:
        _email_log.error("AUTHORISER_NOTIF: email transport not available; cannot send")
        return False

    try:
        _call_transport(send_fn, recipients, subject, body)
        _email_log.info(
            f"✅ authoriser notif sent | order_id={order_id} | order_number={order_number} | band={required_band} | recipients={recipients}"
        )
        return True
    except Exception as e:
        _email_log.error(f"❌ authoriser notif send failed | order_id={order_id} | err={e}")
        return False

# --------------------------
# Minimal finance helper + COD email content
# --------------------------
def _get_finance_recipients() -> List[str]:
    """
    Pick finance recipients robustly:
      1) users.can_receive_payment_notifications = 1, if column exists
      2) users.is_finance = 1, if column exists
      3) users.role/roles IN ('finance','ops','operations','payments','accounts'), if a role column exists
      4) fallback: all users with a non-empty email (deduped)
    """
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(users)")
        cols = {r["name"].lower() for r in cur.fetchall()}

        def _dedupe(rows):
            seen = set(); out = []
            for e in rows:
                e = (e or "").strip()
                if e and e not in seen:
                    out.append(e); seen.add(e)
            return out

        if "can_receive_payment_notifications" in cols:
            cur.execute("SELECT TRIM(COALESCE(email,'')) AS email FROM users WHERE can_receive_payment_notifications = 1")
            return _dedupe([r["email"] for r in cur.fetchall()])

        if "is_finance" in cols:
            cur.execute("SELECT TRIM(COALESCE(email,'')) AS email FROM users WHERE is_finance = 1")
            emails = _dedupe([r["email"] for r in cur.fetchall()])
            if emails:
                return emails

        role_col = "role" if "role" in cols else ("roles" if "roles" in cols else None)
        if role_col:
            cur.execute(f"""
                SELECT TRIM(COALESCE(email,'')) AS email
                FROM users
                WHERE LOWER({role_col}) IN ('finance','ops','operations','payments','accounts')
            """)
            emails = _dedupe([r["email"] for r in cur.fetchall()])
            if emails:
                return emails

        cur.execute("SELECT TRIM(COALESCE(email,'')) AS email FROM users")
        return _dedupe([r["email"] for r in cur.fetchall()])
    
def _build_cod_finance_email(order_number: str, total: float) -> Tuple[str, str]:
    subject = f"COD Order {order_number} ready for payment"
    body = (
        f"COD order {order_number} is ready for payment.\n"
        f"Total: R{total:,.2f}\n\n"
        f"Manage COD orders:\n{_base_url()}/orders/cod_orders\n\n"
        f"— Universal Recycling System"
    )
    return subject, body

def _send_cod_ready_for_payment(order_id: int, total_hint: Optional[float] = None) -> bool:
    """
    Minimal COD finance email. Uses _get_order_header for order_number/total and _get_finance_recipients.
    """
    try:
        order_number, _supplier_name, total, _created_date = _get_order_header(order_id)
        total_use = float(total_hint) if (total_hint is not None) else float(total or 0.0)
    except Exception as e:
        _email_log.error(f"❌ COD mail: order header load failed order_id={order_id}: {e}")
        return False

    recipients = _get_finance_recipients()
    if not recipients:
        _email_log.warning(f"⚠️ COD mail: no finance recipients (set can_receive_payment_notifications=1) order_id={order_id}")
        return False

    subject = f"COD Order {order_number} authorised — ready for payment"
    body = (
        f"Dear colleague,\n\n"
        f"COD Order {order_number} is authorised and ready for payment.\n"
        f"Total: R{total_use:,.2f}\n\n"
        f"Pay / manage COD orders here:\n"
        f"{_base_url()}/orders/cod_orders\n\n"
        f"— Universal Recycling System"
    )

    # Preview
    try:
        _email_log.info(
            "📧 EMAIL PREVIEW | to=%s | subject=%s\n---BODY START---\n%s\n---BODY END---",
            recipients, subject, body
        )
    except Exception:
        pass

    send_fn = _get_transport()
    if not send_fn:
        _email_log.error("❌ email transport not available; cannot send COD finance alert")
        return False

    try:
        _call_transport(send_fn, recipients, subject, body)
        _email_log.info(f"✅ COD finance alert sent | order_id={order_id} | order_number={order_number} | recipients={recipients}")
        return True
    except Exception as e:
        _email_log.error(f"❌ COD finance alert send failed | order_id={order_id} | err={e}")
        return False

# --------------------------
# Public API (lean)
# --------------------------
def dispatch_reviewer_alert_for_creation(order_id: int) -> bool:
    """
    Reviewer alert when an order is created or a draft is submitted for review.
    - Endpoint stays dumb (no recipients/templates).
    - Idempotent per-process.
    - Logs to logs/email_dispatch_log.txt
    """
    key = ("reviewer_alert", int(order_id))
    if key in _SENT:
        _email_log.info(f"🟨 skip duplicate reviewer alert (same process) order_id={order_id}")
        return True
    _SENT.add(key)

    try:
        order_number, supplier_name, total, created_date = _get_order_header(order_id)
    except Exception as e:
        _email_log.error(f"❌ load order header failed order_id={order_id}: {e}")
        return False

    recipients = _get_review_recipients()
    if not recipients:
        _email_log.warning(
            f"⚠️ no reviewer recipients (set can_receive_review_notifications=1) order_id={order_id}"
        )
        return False

    subject, body = _build_reviewer_email(order_number, supplier_name, total)

    # Log full email preview (helps especially when EMAIL_DRY_RUN=1)
    try:
        _email_log.info(
            "📧 EMAIL PREVIEW | to=%s | subject=%s\n---BODY START---\n%s\n---BODY END---",
            recipients, subject, body
        )
    except Exception:
        # Never block sending on logging issues
        pass

    send_fn = _get_transport()
    if not send_fn:
        _email_log.error("❌ email transport not available; cannot send reviewer alert")
        return False

    try:
        _call_transport(send_fn, recipients, subject, body)
        _email_log.info(
            f"✅ reviewer alert sent | order_id={order_id} | order_number={order_number} | "
            f"recipients={recipients} | created_at={created_date or now_utc_iso()}"
        )
        return True
    except Exception as e:
        _email_log.error(f"❌ reviewer alert send failed | order_id={order_id} | err={e}")
        return False

# Back-compat names some callers probe:
dispatch_reviewer_alert = dispatch_reviewer_alert_for_creation
send_reviewer_alert_for_creation = dispatch_reviewer_alert_for_creation
send_reviewer_alert = dispatch_reviewer_alert_for_creation

# --------------------------
# Supplier Notification
# --------------------------
def _get_order_details_for_supplier(order_id: int):
    """
    Get full order details including supplier info, business details, and line items.
    Returns dict with all info needed for supplier email.
    """
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Get order + supplier + business details
        cur.execute("""
            SELECT
                o.order_number,
                o.created_date,
                o.total,
                o.note_to_supplier,
                o.payment_terms,
                s.name AS supplier_name,
                s.email AS supplier_email,
                s.contact_name AS supplier_contact,
                b.company_name,
                b.address_line1,
                b.address_line2,
                b.city,
                b.province,
                b.postal_code,
                b.telephone AS company_telephone
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN business_details b ON b.id = 1
            WHERE o.id = ?
        """, (order_id,))
        order_row = cur.fetchone()

        if not order_row:
            raise ValueError(f"Order {order_id} not found")

        # Get order line items
        cur.execute("""
            SELECT
                item_code,
                item_description,
                qty_ordered,
                price,
                total
            FROM order_items
            WHERE order_id = ?
            ORDER BY id
        """, (order_id,))
        items = cur.fetchall()

        return {
            'order_number': order_row['order_number'],
            'created_date': order_row['created_date'],
            'total': float(order_row['total'] or 0.0),
            'note_to_supplier': order_row['note_to_supplier'],
            'payment_terms': order_row['payment_terms'] or 'On account',
            'supplier_name': order_row['supplier_name'],
            'supplier_email': order_row['supplier_email'],
            'supplier_contact': order_row['supplier_contact'],
            'company_name': order_row['company_name'],
            'company_address': f"{order_row['address_line1']}, {order_row['address_line2']}, {order_row['city']}, {order_row['province']} {order_row['postal_code']}",
            'company_telephone': order_row['company_telephone'],
            'items': items
        }

def _build_supplier_email(details: dict) -> Tuple[str, str, str]:
    """
    Build professional supplier notification email with HTML and logo.
    Returns (subject, plain_body, html_body)
    """
    # Format contact name
    contact = details['supplier_contact'] or "Procurement Team"

    # Format date
    order_date = details['created_date'][:10] if details['created_date'] else now_utc_iso()[:10]

    # Subject
    subject = f"New Purchase Order #{details['order_number']} from {details['company_name']}"

    # Plain text version (fallback)
    items_text = "\n"
    for item in details['items']:
        item_code = item['item_code'] or ''
        desc = item['item_description'] or ''
        qty = float(item['qty_ordered'] or 0)
        price = float(item['price'] or 0)
        total = float(item['total'] or 0)
        items_text += f"  • {item_code} - {desc}\n"
        items_text += f"    Quantity: {qty:,.2f} | Unit Price: R{price:,.2f} | Total: R{total:,.2f}\n"

    plain_body = f"""Dear {contact},

This email confirms the placement of Purchase Order #{details['order_number']} by {details['company_name']}.

PO Number: {details['order_number']}
Order Date: {order_date}
Total Value: R{details['total']:,.2f}
Payment Terms: {details['payment_terms']}

Items:{items_text}

Sincerely,
Procurement Department
{details['company_name']}
"""

    # HTML version with items table
    items_html = ""
    for item in details['items']:
        items_html += f"""<tr>
            <td>{item['item_code'] or ''}</td>
            <td>{item['item_description'] or ''}</td>
            <td align="right">{float(item['qty_ordered'] or 0):,.2f}</td>
            <td align="right">R{float(item['price'] or 0):,.2f}</td>
            <td align="right">R{float(item['total'] or 0):,.2f}</td>
        </tr>"""

    note_html = ""
    if details['note_to_supplier']:
        note_html = f"""<div style="background:#fff3cd;border-left:4px solid #ffc107;padding:15px;margin:20px 0">
            <h3 style="margin-top:0;color:#856404">⚠️ Special Instructions</h3>
            <p style="margin:0">{details['note_to_supplier'].replace(chr(10), '<br>')}</p>
        </div>"""

    logo = "data:image/jpeg;base64,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"

    html_body = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;line-height:1.6;color:#333;max-width:800px;margin:0 auto;padding:20px">
<div style="background:#f8f9fa;padding:20px;border-bottom:3px solid #007bff">
    <img src="{logo}" alt="Logo" style="width:140px;margin-bottom:10px">
    <h1 style="color:#007bff;margin:10px 0;font-size:24px">Purchase Order #{details['order_number']}</h1>
    <p style="margin:5px 0"><strong>{details['company_name']}</strong></p>
    <p style="margin:5px 0">{details['company_address']}</p>
    <p style="margin:5px 0">Tel: {details['company_telephone']}</p>
</div>
<p>Dear {contact},</p>
<p>This email confirms the placement of <strong>Purchase Order #{details['order_number']}</strong> by {details['company_name']}.</p>
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr><th style="background:#007bff;color:white;padding:12px;text-align:left">PO Number</th><td style="padding:10px;border:1px solid #ddd">{details['order_number']}</td></tr>
<tr><th style="background:#007bff;color:white;padding:12px;text-align:left">Order Date</th><td style="padding:10px;border:1px solid #ddd">{order_date}</td></tr>
<tr><th style="background:#007bff;color:white;padding:12px;text-align:left">Total Value</th><td style="padding:10px;border:1px solid #ddd"><strong>R{details['total']:,.2f}</strong></td></tr>
<tr><th style="background:#007bff;color:white;padding:12px;text-align:left">Payment Terms</th><td style="padding:10px;border:1px solid #ddd">{details['payment_terms']}</td></tr>
<tr><th style="background:#007bff;color:white;padding:12px;text-align:left">Delivery Address</th><td style="padding:10px;border:1px solid #ddd">{details['company_address']}</td></tr>
</table>
<h2 style="color:#007bff">Items Ordered</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<thead><tr>
<th style="background:#007bff;color:white;padding:10px;text-align:left">Item Code</th>
<th style="background:#007bff;color:white;padding:10px;text-align:left">Description</th>
<th style="background:#007bff;color:white;padding:10px;text-align:right">Quantity</th>
<th style="background:#007bff;color:white;padding:10px;text-align:right">Unit Price</th>
<th style="background:#007bff;color:white;padding:10px;text-align:right">Total</th>
</tr></thead>
<tbody>{items_html}</tbody>
</table>
{note_html}
<div style="background:#e7f3ff;padding:20px;margin:20px 0;border-radius:5px">
<h3 style="color:#007bff;margin-top:0">Next Steps</h3>
<ol style="margin:10px 0;padding-left:20px">
<li style="margin:8px 0"><strong>CONFIRMATION:</strong> Please acknowledge receipt within 2 business days.</li>
<li style="margin:8px 0"><strong>PROCESSING:</strong> Please proceed with fulfillment as specified.</li>
<li style="margin:8px 0"><strong>INVOICING:</strong> Reference PO #{details['order_number']} on all invoices and shipping documents.</li>
</ol>
</div>
<p>Questions? Contact our Procurement Department at <strong>{details['company_telephone']}</strong></p>
<div style="margin-top:30px;padding-top:20px;border-top:1px solid #ddd;color:#666">
<p><strong>Sincerely,</strong></p>
<p>Procurement Department<br>{details['company_name']}<br>{details['company_telephone']}</p>
</div>
</body></html>"""

    return subject, plain_body, html_body

def send_supplier_notification(order_id: int) -> bool:
    """
    Send purchase order notification to supplier.
    Called when an order is fully authorized and ready to be sent to the supplier.
    """
    key = ("supplier_notification", int(order_id))
    if key in _SENT:
        _email_log.info(f"🟨 skip duplicate supplier notification (same process) order_id={order_id}")
        return True
    _SENT.add(key)

    try:
        details = _get_order_details_for_supplier(order_id)
    except Exception as e:
        _email_log.error(f"❌ supplier notification: failed to load order details order_id={order_id}: {e}")
        return False

    # Check if supplier has email
    if not details['supplier_email']:
        _email_log.warning(f"⚠️ supplier notification: no email for supplier order_id={order_id} | order_number={details['order_number']}")
        return False

    supplier_email = details['supplier_email'].strip()

    subject, plain_body, html_body = _build_supplier_email(details)

    # Log preview
    try:
        _email_log.info(
            "📧 SUPPLIER EMAIL PREVIEW | to=%s | subject=%s\n---BODY START---\n%s\n---BODY END---",
            supplier_email, subject, body
        )
    except Exception:
        pass

    send_fn = _get_transport()
    if not send_fn:
        _email_log.error("❌ supplier notification: email transport not available")
        return False

    try:
        send_fn([supplier_email], subject, plain_body, html_body)
        _email_log.info(
            f"✅ supplier notification sent | order_id={order_id} | order_number={details['order_number']} | "
            f"supplier={details['supplier_name']} | recipient={supplier_email}"
        )
        return True
    except Exception as e:
        _email_log.error(f"❌ supplier notification send failed | order_id={order_id} | err={e}")
        return False

# --------------------------
# Public API (lean)
# --------------------------
def dispatch(triggers: Iterable[Any]):
    """
    Minimal router:
      - Handle COD_READY_FOR_PAYMENT
      - Handle AUTHORISER_NOTIF
      - Skip anything else (clean log; we can add more later)
    """
    try:
        _trigs = list(triggers)
    except TypeError:
        _trigs = [*triggers]

    for t in _trigs:
        evt = getattr(t, "event", None)
        evt_name = getattr(evt, "name", str(evt) if evt is not None else "")
        order_id = int(getattr(t, "order_id", 0) or 0)
        ctx = getattr(t, "context", {}) or {}
        key = (evt_name, order_id)

        # Idempotency within this process
        if key in _SENT:
            _email_log.info(f"🟨 skip duplicate {evt_name} for order_id={order_id}")
            continue
        _SENT.add(key)

        if evt_name == "COD_READY_FOR_PAYMENT":
            _send_cod_ready_for_payment(order_id, total_hint=ctx.get("total"))
        elif evt_name == "AUTHORISER_NOTIF":
            _send_authoriser_notif(
                order_id,
                required_band=ctx.get("required_band"),
                total_hint=ctx.get("total"),
            )
        elif evt_name == "SUPPLIER_NOTIFICATION":
            send_supplier_notification(order_id)
        else:
            _email_log.info(
                f"ℹ️ skipping unsupported email event {evt_name} for order_id={order_id} (will add later)"
            )
    return
