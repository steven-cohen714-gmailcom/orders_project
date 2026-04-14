# backend/utils/email_and_alerts_engine.py
from __future__ import annotations

import asyncio
import inspect
import logging
import os
from typing import Iterable, List, Dict, Any, Optional, Tuple, Set
import sqlite3
from backend.database import get_db_connection

from .flows_types import EmailEventType, EmailTrigger

from backend.utils.statuses import (
    AWAITING_AUTHORISATION,
    AUTHORISED,
    PARTIALLY_PAID,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment / Config
# ---------------------------------------------------------------------------

import os  # keep a single import; safe if also imported above
def _base_url() -> str:
    # Read at call-time (not import-time) so value can differ per machine/process
    return (os.getenv("FRONTEND_BASE_URL") or os.getenv("APP_BASE_URL") or "http://localhost:8004").rstrip("/")

# In-process idempotency: prevents accidental duplicates per process lifetime
# Key format: f"{event}|{order_id}"
_SENT_KEYS: Set[str] = set()

# Try to import the low-level mailer. It may be async.
try:
    from .send_email import send_email as _smtp_send_email  # type: ignore
except Exception as e:  # pragma: no cover
    _smtp_send_email = None
    logger.warning("send_email import failed: %s", e)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def dispatch(triggers: Iterable[EmailTrigger]) -> None:
    """
    Central email router. Accepts semantic triggers and fans out to concrete emails.
    Decides recipients, subjects/bodies, and batching of context lists.
    - Idempotency: prevents duplicate sends for the same (event, order_id) burst.
    """

    # Materialize once so we can count safely and avoid iterator reuse issues
    try:
        _trigs = list(triggers)
    except TypeError:
        _trigs = [*triggers]

    logger.debug("EMAIL_DISPATCH incoming_count=%s", len(_trigs))

    for t in _trigs:
        # Build a stable idempotency key
        evt = getattr(t.event, "name", str(t.event))
        oid = getattr(t, "order_id", None)
        key = f"{evt}|{oid if oid is not None else 'none'}"

        # Skip if we've already handled this (event, order)
        if key in _SENT_KEYS:
            logger.info("EMAIL_SKIP_DUP idempotent=%s", key)
            continue

        # Mark as handled BEFORE sending to prevent stampede duplicates
        _SENT_KEYS.add(key)

        try:
            if t.event is EmailEventType.AUTHORISER_NOTIF:
                _handle_authoriser_notif(t)
            elif t.event is EmailEventType.COD_READY_FOR_PAYMENT:
                _handle_cod_ready_for_payment(t)
            elif t.event is EmailEventType.REVIEWER_CONFIRMATION:
                _handle_reviewer_confirmation(t)
            else:
                logger.warning("Unknown EmailEventType: %s", t.event)
                # Unknown: allow future attempts
                _SENT_KEYS.discard(key)
                continue

        except Exception as e:
            # Error: allow a future retry by removing the key
            _SENT_KEYS.discard(key)
            logger.exception(
                "EMAIL_DISPATCH_ERROR event=%s order_id=%s err=%s",
                t.event, getattr(t, "order_id", None), e
            )
            # Do not re-raise; we don't want to 500 the caller due to email failure.

# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------

def _handle_authoriser_notif(t: EmailTrigger) -> None:
    order = _get_order_meta(t.order_id)
    required_band = (t.context or {}).get("required_band")
    total = (t.context or {}).get("total")

    recipients = _get_authorisers_for_band(required_band)
    if not recipients:
        logger.info("AUTHORISER_NOTIF: no recipients for band=%s order_id=%s", required_band, t.order_id)
        return

    # Build "other orders you can authorise now" for each recipient (personalised)
    for user in recipients:
        user_id, email, name = user
        others = _list_authorisable_orders_for_user(user_id, limit=10, exclude_order_id=t.order_id)

        subject = f"Order {order['order_number']} requires Band {required_band} authorisation"
        lines = [
            f"Dear {name or 'Approver'},",
            "",
            f"Order {order['order_number']} requires Band {required_band} authorisation.",
            f"Total: {order['currency']}{_fmt_money(total or order['total'])}",
            "",
            f"Review & authorise here:",
            f"{_base_url()}/orders/authorisations",
        ]
        if others:
            lines += [
                "",
                "Other orders you can authorise now:"
            ]
            for o in others:
                lines.append(f"- Order {o['order_number']} (Band {o['required_band']}, {o['currency']}{_fmt_money(o['total'])})")

        lines += ["", "— Universal Recycling System"]
        body = "\n".join(lines)

        _send_mail(email, subject, body)


def _handle_cod_ready_for_payment(t: EmailTrigger) -> None:
    order = _get_order_meta(t.order_id)
    total = (t.context or {}).get("total", order["total"])
    recipients = _get_finance_recipients()
    if not recipients:
        logger.info("COD_READY_FOR_PAYMENT: no finance recipients order_id=%s", t.order_id)
        return

    others = _list_cod_ready_orders(limit=20, exclude_order_id=t.order_id)

    subject = f"COD Order {order['order_number']} authorised — ready for payment"
    list_lines = []
    if others:
        list_lines.append("")
        list_lines.append("Other COD orders currently ready for payment:")
        for o in others:
            list_lines.append(f"- Order {o['order_number']} ({o['currency']}{_fmt_money(o['total'])})")

    body_template = (
        "Dear {name},\n\n"
        "COD Order (Order Number: {order_number}, Total: {currency}{total}) has been authorised and is now ready for payment.\n\n"
        "Pay / manage COD orders here:\n"
        "{cod_url}\n"
        "{other_lines}\n\n"
        "Kind regards,\n"
        "Universal Recycling System"
    )

    for user_id, email, name in recipients:
        body = body_template.format(
            name=name or "colleague",
            order_number=order["order_number"],
            currency=order["currency"],
            total=_fmt_money(total),
            cod_url=f"{_base_url()}/orders/cod_orders",
            other_lines=("\n" + "\n".join(list_lines)) if list_lines else "",
        )
        _send_mail(email, subject, body)


def _handle_reviewer_confirmation(t: EmailTrigger) -> None:
    order = _get_order_meta(t.order_id)
    routed_to = (t.context or {}).get("routed_to")
    required_band = (t.context or {}).get("required_band")
    total = (t.context or {}).get("total", order["total"])

    email = _get_user_email(t.actor_user_id)
    if not email:
        return

    subject = f"Reviewed: {order['order_number']} → {routed_to}"
    lines = [
        f"Dear { _get_user_name(t.actor_user_id) or 'colleague' },",
        "",
        f"You reviewed Order {order['order_number']} "
        f"and it was routed to '{routed_to}'" + (f" (Band {required_band})" if required_band else "") + ".",
        f"Total: {order['currency']}{_fmt_money(total)}",
        "",
        f"Open Review/Authorisations:",
        f"{_base_url()}/orders/authorisations",
        "",
        "— Universal Recycling System",
    ]
    body = "\n".join(lines)
    _send_mail(email, subject, body)


# ---------------------------------------------------------------------------
# Mail transport (handles async/sync function)
# ---------------------------------------------------------------------------

def _send_mail(recipient: str, subject: str, body: str) -> None:

    if not _smtp_send_email:
        logger.error("send_email is not available; cannot send")
        return

    try:
        if inspect.iscoroutinefunction(_smtp_send_email):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(_smtp_send_email(recipient, subject, body))
                else:
                    loop.run_until_complete(_smtp_send_email(recipient, subject, body))
            except RuntimeError:
                # No running loop
                asyncio.run(_smtp_send_email(recipient, subject, body))
        else:
            _smtp_send_email(recipient, subject, body)  # type: ignore
    except Exception as e:
        logger.exception("EMAIL_SEND_FAILED to=%s subject=%s err=%s", recipient, subject, e)


# ---------------------------------------------------------------------------
# Data lookups (SAFE STUBS — replace with real DB queries)
# Keep signatures stable. Return empty lists if unknown; engine still works.
# ---------------------------------------------------------------------------

def _get_order_meta(order_id: int) -> Dict[str, Any]:
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT order_number, total, COALESCE(payment_terms,'') AS terms
            FROM orders
            WHERE id = ?
        """, (order_id,))
        row = cur.fetchone()
        if not row:
            return {"order_number": str(order_id), "total": 0.0, "currency": "R", "is_cod": False, "required_band": None}

        terms = (row["terms"] or "").strip().upper()
        is_cod = (terms == "COD" or terms == "CASH ON DELIVERY" or "COD" in terms)
        return {
            "order_number": row["order_number"],
            "total": float(row["total"] or 0),
            "currency": "R",
            "is_cod": is_cod,
            "required_band": None,  # (not needed here; included in trigger context when relevant)
        }
    except Exception:
        return {"order_number": str(order_id), "total": 0.0, "currency": "R", "is_cod": False, "required_band": None}
    finally:
        conn.close()

def _get_authorisers_for_band(required_band: Optional[int]) -> List[Tuple[int, str, str]]:
    """
    Returns list of (user_id, email, display_name) who can authorise for this band.
    Detects the band column automatically: auth_threshold_band / threshold_band / authorisation_band / auth_band.
    """
    if required_band is None:
        return []

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cols = {r["name"].lower() for r in cur.execute("PRAGMA table_info(users)")}
        # Pick whichever band column exists
        band_col = None
        for c in ("auth_threshold_band", "threshold_band", "authorisation_band", "auth_band"):
            if c in cols:
                band_col = c
                break
        if not band_col:
            logger.warning("No band column on users table; cannot find authorisers")
            return []

        name_expr = "COALESCE(display_name, name, username, email)"
        active_filter = "AND active = 1" if "active" in cols else ""

        sql = f"""
            SELECT id AS user_id, email, {name_expr} AS display_name
            FROM users
            WHERE email IS NOT NULL AND email <> ''
              AND {band_col} IS NOT NULL
              AND CAST({band_col} AS INTEGER) >= CAST(? AS INTEGER)
              {active_filter}
            ORDER BY CAST({band_col} AS INTEGER) DESC, id ASC
        """
        cur.execute(sql, (required_band,))
        return [(int(r["user_id"]), r["email"], r["display_name"]) for r in cur.fetchall()]
    except Exception:
        return []
    finally:
        conn.close()

def _list_authorisable_orders_for_user(user_id: int, limit: int = 10, exclude_order_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Orders the user can authorise now:
    status='Awaiting Authorisation' AND required_auth_band <= user's band.
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        # Get the user's band
        cur.execute("SELECT auth_threshold_band FROM users WHERE id = ?", (user_id,))
        r = cur.fetchone()
        if not r or r["auth_threshold_band"] is None:
            return []
        try:
            user_band = int(r["auth_threshold_band"])
        except Exception:
            return []

        # Build params
        params: List[Any] = [user_band]
        exclude_sql = ""
        if exclude_order_id is not None:
            exclude_sql = "AND o.id <> ?"
            params.append(exclude_order_id)
        params.append(int(limit))

        # Correct query for authorisable orders
        sql = f"""
            SELECT
                o.order_number,
                o.required_auth_band AS required_band,
                o.total
            FROM orders o
            WHERE o.status = ?
              AND o.required_auth_band IS NOT NULL
              AND CAST(o.required_auth_band AS INTEGER) <= CAST(? AS INTEGER)
              {exclude_sql}
            ORDER BY datetime(COALESCE(o.created_date,'1970-01-01')) DESC, o.id DESC
            LIMIT ?
        """
        cur.execute(sql, tuple(params))

        rows = cur.fetchall()
        out: List[Dict[str, Any]] = []
        for row in rows:
            rb = int(row["required_band"]) if row["required_band"] is not None else None
            out.append({
                "order_number": row["order_number"],
                "required_band": rb,
                "total": float(row["total"] or 0.0),
                "currency": "R",
            })
        return out

    except Exception:
        return []
    finally:
        conn.close()

def _get_finance_recipients() -> List[Tuple[int, str, str]]:
    """
    Finance/ops recipients for COD notifications.
    Tries (in order): users.is_finance=1; role IN ('finance','ops','payments'); can_pay_cod=1; else all with email.
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cols = {r["name"].lower() for r in cur.execute("PRAGMA table_info(users)")}

        name_expr = "COALESCE(display_name, name, username, email)"
        active_filter = "AND active = 1" if "active" in cols else ""
        results: List[Tuple[int, str, str]] = []

        # 0) Prefer your existing flag, when present
        if "can_receive_payment_notifications" in cols:
            cur.execute(f"""
                SELECT id, email, {name_expr} AS display_name
                FROM users
                WHERE email IS NOT NULL AND email <> ''
                  AND can_receive_payment_notifications = 1
                  {active_filter}
            """)
            results = [(int(r["id"]), r["email"], r["display_name"]) for r in cur.fetchall()]
            if results:
                return results

        # 1) is_finance
        if "is_finance" in cols:
            cur.execute(f"""
                SELECT id, email, {name_expr} AS display_name
                FROM users
                WHERE email IS NOT NULL AND email <> ''
                  AND is_finance = 1
                  {active_filter}
            """)
            results = [(int(r["id"]), r["email"], r["display_name"]) for r in cur.fetchall()]
            if results:
                return results

        # 2) role/roles IN (...)
        if "role" in cols or "roles" in cols:
            role_col = "role" if "role" in cols else "roles"
            cur.execute(f"""
                SELECT id, email, {name_expr} AS display_name
                FROM users
                WHERE email IS NOT NULL AND email <> ''
                  AND LOWER({role_col}) IN ('finance','ops','operations','payments','accounts')
                  {active_filter}
            """)
            results = [(int(r["id"]), r["email"], r["display_name"]) for r in cur.fetchall()]
            if results:
                return results


        # 4) Fallback: all users with email (filtered by active if present)
        cur.execute(f"""
            SELECT id, email, {name_expr} AS display_name
            FROM users
            WHERE email IS NOT NULL AND email <> ''
            {active_filter}
        """)
        return [(int(r["id"]), r["email"], r["display_name"]) for r in cur.fetchall()]

    except Exception:
        return []
    finally:
        conn.close()

def _list_cod_ready_orders(limit: int = 20, exclude_order_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    COD orders authorised and not fully paid.
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        params: List[Any] = []
        exclude_sql = ""
        if exclude_order_id is not None:
            exclude_sql = "AND o.id <> ?"
            params.append(exclude_order_id)

        params.append(int(limit))

        cur.execute(f"""
            SELECT o.order_number, o.total
            FROM orders o
            WHERE UPPER(COALESCE(o.payment_terms,'')) = 'COD'
              AND o.status IN (?, ?)
              {exclude_sql}
            ORDER BY datetime(o.created_date) DESC, o.id DESC
            LIMIT ?
        """, tuple(params))
        out = []
        for r in cur.fetchall():
            out.append({
                "order_number": r["order_number"],
                "total": float(r["total"] or 0),
                "currency": "R",
            })
        return out
    except Exception:
        return []
    finally:
        conn.close()

def _get_user_email(user_id: Optional[int]) -> Optional[str]:
    if not user_id:
        return None
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        r = cur.fetchone()
        if not r:
            return None
        email = (r["email"] or "").strip()
        return email or None
    except Exception:
        return None
    finally:
        conn.close()

def _get_user_name(user_id: Optional[int]) -> Optional[str]:
    if not user_id:
        return None
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(users)")
        cols = {r["name"].lower() for r in cur.fetchall()}
        name_expr = "display_name" if "display_name" in cols else ("name" if "name" in cols else "username")
        cur.execute(f"SELECT {name_expr} AS n FROM users WHERE id = ?", (user_id,))
        r = cur.fetchone()
        if not r:
            return None
        n = r["n"]
        if not n:
            return None
        return str(n)
    except Exception:
        return None
    finally:
        conn.close()

# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------

def _fmt_money(x: Any) -> str:
    try:
        return f"{float(x):,.2f}"
    except Exception:
        return str(x)
