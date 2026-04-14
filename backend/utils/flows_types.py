# backend/utils/flows_types.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class EmailEventType(Enum):
    """Semantic events. The email engine resolves recipients & templates."""
    AUTHORISER_NOTIF = auto()         # After Review -> Awaiting Authorisation
    COD_READY_FOR_PAYMENT = auto()    # After Authorised (and COD)
    REVIEWER_CONFIRMATION = auto()    # Optional: reviewer opted to get a copy


@dataclass(frozen=True)
class EmailTrigger:
    """
    A high-level signal for the email engine.
    Do NOT include recipients/subjects here—email engine decides that.
    """
    event: EmailEventType
    order_id: int
    actor_user_id: Optional[int] = None   # who performed the action (reviewer/authoriser)
    context: Optional[Dict[str, Any]] = None  # optional extra info (band, totals, etc.)


@dataclass(frozen=True)
class DecisionResult:
    """
    Output from the authorisation engine after a state-changing action.
    All writes (status, band) should be persisted by the caller using these values.
    """
    new_status: str
    required_auth_band: Optional[int]
    audit_rows: List[str]
    email_triggers: List[EmailTrigger]
    cod_tick_enabled: bool  # UI rule for COD screen
