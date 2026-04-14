# File: backend/utils/statuses.py
from __future__ import annotations

from typing import Optional

# -----------------------------------------------------------------------------
# Canonical statuses (DB stores these exact strings)
# -----------------------------------------------------------------------------
DRAFT = "Draft"
FOR_REVIEW = "For Review"

# After review:
AWAITING_AUTHORISATION = "Awaiting Authorisation"   # required_auth_band != NULL
PENDING = "Pending"                                  # under-threshold after review

# Authorisation outcomes:
AUTHORISED = "Authorised"
DECLINED = "Declined"

# Receiving:
RECEIVED = "Received"
PARTIALLY_RECEIVED = "Partially Received"

# Payments:
PARTIALLY_PAID = "Partially Paid"                    # COD/payment flow only
FULLY_PAID = "Fully Paid"                            # COD/payment flow only

# Admin:
DELETED = "Deleted"

# -----------------------------------------------------------------------------
# Status groupings / sets
# -----------------------------------------------------------------------------
PAYMENT_STATUSES = {PARTIALLY_PAID, FULLY_PAID}
RECEIPT_STATUSES = {PARTIALLY_RECEIVED, RECEIVED}
ON_HOLD = "On Hold"  # legacy alias to satisfy old imports

# Allowed to perform receiving from these states (matches endpoint logic)
ALLOWED_TO_RECEIVE_FROM = {PENDING, AUTHORISED, PARTIALLY_RECEIVED, PARTIALLY_PAID, FULLY_PAID}

# Terminal = no further business flow expected
TERMINAL_STATUSES = {DECLINED, FULLY_PAID, DELETED}

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def cod_tick_enabled(status: str) -> bool:
    """
    COD 'tick' is disabled until an order is Authorised.
    After Authorised, tick is enabled; payment flow can move to Partially/Fully Paid.
    """
    return status == AUTHORISED or status in PAYMENT_STATUSES


def can_user_authorise(required_band: Optional[int], user_band: Optional[int]) -> bool:
    """
    Authorisations queue visibility/action rule:
    - If required_band is None -> nothing to authorise (shouldn't be in queue).
    - User can authorise when user_band is not None and user_band >= required_band.
    """
    if required_band is None or user_band is None:
        return False
    try:
        return int(user_band) >= int(required_band)
    except Exception:
        return False


def is_under_threshold(required_band: Optional[int]) -> bool:
    """Under threshold == no band required at all (None)."""
    return required_band is None
