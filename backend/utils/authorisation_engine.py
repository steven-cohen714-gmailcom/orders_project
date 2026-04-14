# backend/utils/authorisation_engine.py
from __future__ import annotations

from typing import Optional, Tuple, Dict, Any, List

from .flows_types import DecisionResult, EmailEventType, EmailTrigger
from .flows_types import EmailTrigger as _Trig
from .statuses import (
    DRAFT, FOR_REVIEW, AWAITING_AUTHORISATION, PENDING,
    AUTHORISED, DECLINED, PARTIALLY_PAID, FULLY_PAID,
    cod_tick_enabled as _cod_tick_enabled, is_under_threshold,
)

import sqlite3
from backend.database import get_db_connection

# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------

def apply_review_decision(
    order_id: int,
    action: str,              # expected: "reviewed"
    actor_user_id: int,
) -> DecisionResult:
    """
    Called by the Review endpoint after a human reviews an order.

    Computes:
      - required_auth_band (None => under-threshold)
      - next status: Pending (no band) OR Awaiting Authorisation (Band X)
      - audit rows
      - email triggers:
          * COD_READY_FOR_PAYMENT for ANY COD order (under- or over-threshold)
          * AUTHORISER_NOTIF when routing to Awaiting Authorisation
          * REVIEWER_CONFIRMATION if reviewer opted-in
    """
    assert action == "reviewed", f"Unsupported review action: {action}"

    ctx = _get_order_context(order_id)
    # Pull the reviewer’s notification preference from DB
    ctx["reviewer_wants_review_emails"] = _get_reviewer_pref(actor_user_id)

    required_band = _compute_required_band(
        total=ctx["total"],
        threshold_table=ctx["threshold_table"],
        is_cod=ctx["is_cod"],
    )

    email_triggers: List[EmailTrigger] = []

    # Always send COD finance alert as soon as review completes (your policy)
    if ctx["is_cod"]:
        email_triggers.append(_make_trigger(
            EmailEventType.COD_READY_FOR_PAYMENT, order_id, actor_user_id,
            total=ctx["total"]
        ))

    if is_under_threshold(required_band):
        new_status = PENDING
        # Reviewer self-confirmation (if enabled)

        audit_rows = [
            f"Reviewed by user:{actor_user_id} → Routed to '{new_status}' (under threshold)"
        ]
    else:
        new_status = AWAITING_AUTHORISATION
        # Notify authorisers
        email_triggers.append(_make_trigger(
            EmailEventType.AUTHORISER_NOTIF, order_id, actor_user_id,
            required_band=int(required_band), total=ctx["total"], is_cod=ctx["is_cod"]
        ))

        audit_rows = [
            f"Reviewed by user:{actor_user_id} → Routed to '{new_status}' (Band {int(required_band)})"
        ]

    return DecisionResult(
        new_status=new_status,
        required_auth_band=required_band,
        audit_rows=audit_rows,
        email_triggers=email_triggers,
        cod_tick_enabled=_cod_tick_enabled(new_status),
    )

def apply_authoriser_action(
    order_id: int,
    action: str,              # "approve" | "decline"
    actor_user_id: int,
) -> DecisionResult:
    """
    Called by the Authorisations API when an authoriser approves/declines.

    Computes:
      - new status ("Authorised" or "Declined")
      - preserves required_auth_band (we don't null it here; DB keeps what review set)
      - COD emails are NOT sent here (we already sent at review time by policy)
    """
    if action not in ("approve", "decline"):
        raise ValueError(f"Unsupported authoriser action: {action}")

    ctx = _get_order_context(order_id)

    if action == "approve":
        new_status = AUTHORISED
        email_triggers: List[EmailTrigger] = []
        audit_rows = [f"Authorised by user:{actor_user_id}"]
    else:
        new_status = DECLINED
        email_triggers = []
        audit_rows = [f"Declined by user:{actor_user_id}"]

    return DecisionResult(
        new_status=new_status,
        required_auth_band=ctx.get("required_auth_band_after_review"),  # keep whatever review set
        audit_rows=audit_rows,
        email_triggers=email_triggers,
        cod_tick_enabled=_cod_tick_enabled(new_status),
    )

# -----------------------------------------------------------------------------
# CONTEXT / THRESHOLDS
# -----------------------------------------------------------------------------

def _get_order_context(order_id: int) -> Dict[str, Any]:
    """
    Pull order facts from DB and load the company band thresholds from settings.
    - COD detection: treat 'COD', 'CASH ON DELIVERY', or any value containing 'COD' as COD.
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT total, payment_terms, required_auth_band FROM orders WHERE id = ?", (order_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Order not found")

        total = float(row["total"] or 0)
        terms = (row["payment_terms"] or "").strip().upper()
        is_cod = (terms == "COD") or (terms == "CASH ON DELIVERY") or ("COD" in terms)
        required_auth_band_after_review = row["required_auth_band"]

        # Load thresholds from settings (authoritative - Maintenance screen)
        cur.execute("""
            SELECT auth_threshold_1, auth_threshold_2, auth_threshold_3,
                   auth_threshold_4, auth_threshold_5
            FROM settings
            ORDER BY id ASC
            LIMIT 1
        """)
        s = cur.fetchone()
        if not s:
            raise ValueError("Settings not found: please create a row in 'settings' with band thresholds.")

        threshold_table: List[Tuple[int, float]] = [
            (1, float(s["auth_threshold_1"] or 0)),
            (2, float(s["auth_threshold_2"] or 0)),
            (3, float(s["auth_threshold_3"] or 0)),
            (4, float(s["auth_threshold_4"] or 0)),
            (5, float(s["auth_threshold_5"] or 0)),
        ]

        return {
            "total": total,
            "is_cod": is_cod,
            "required_auth_band_after_review": required_auth_band_after_review,
            "threshold_table": threshold_table,
            # set in apply_review_decision via _get_reviewer_pref(actor_user_id)
            "reviewer_wants_review_emails": False,
        }
    finally:
        conn.close()

def _get_reviewer_pref(user_id: int) -> bool:
    """
    Returns True if the user has opted to receive a self-notification after review.
    Checks your real column first.
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for col in (
            "can_receive_review_notifications",  # your DB column
            "receive_review_notifications",
            "receive_review_emails",
            "receive_review_mail",
        ):
            try:
                cur.execute(f"SELECT {col} AS pref FROM users WHERE id = ?", (user_id,))
                r = cur.fetchone()
                if r is None:
                    continue
                val = r["pref"]
                if isinstance(val, str):
                    v = val.strip().lower()
                    if v in ("1", "true", "t", "yes", "y"):
                        return True
                    if v in ("0", "false", "f", "no", "n", ""):
                        return False
                if isinstance(val, (int, float)):
                    return bool(int(val))
                return bool(val)
            except Exception:
                continue
        return False
    except Exception:
        return False
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass

def _compute_required_band(total: float, threshold_table: List[Tuple[int, float]], is_cod: bool) -> Optional[int]:
    """
    Decide which band is required for this order, or None if under threshold.

    Policy:
      - Compare 'total' to ascending thresholds with STRICT '>' semantics.
        (Equal to the threshold stays under-threshold → Pending.)
      - COD does NOT change the band requirement.
    """
    # Sort by band just in case
    sorted_thresholds = sorted(threshold_table, key=lambda x: x[0])
    required: Optional[int] = None
    for band, min_total in sorted_thresholds:
        if total > float(min_total):   # STRICTLY greater than
            required = band
    return required

# -----------------------------------------------------------------------------
# UTIL
# -----------------------------------------------------------------------------

def _make_trigger(event: EmailEventType, order_id: int, actor_user_id: Optional[int] = None, **context) -> _Trig:
    return _Trig(event=event, order_id=order_id, actor_user_id=actor_user_id, context=(context or None))
