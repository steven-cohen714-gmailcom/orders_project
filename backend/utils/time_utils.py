# backend/utils/time_utils.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

ISO_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

def now_utc_iso() -> str:
    """Return UTC timestamp as ISO8601 with Z, millisecond-ish precision (trim microseconds to 3)."""
    dt = datetime.now(timezone.utc)
    # Trim to milliseconds to keep strings shorter/consistent
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(dt.microsecond/1000):03d}Z"

def to_utc_iso(dt: datetime) -> str:
    """Coerce any aware/naive datetime to UTC ISO8601 Z string."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)  # assume already UTC if naive
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(dt.microsecond/1000):03d}Z"

def parse_iso_z(s: str) -> datetime:
    """Parse an ISO8601 string with trailing Z to an aware UTC datetime."""
    # Support both xxxxZ and xxxx.xxxZ lengths
    if s.endswith("Z") and "." not in s:
        # add .000 for strict parsing
        s = s[:-1] + ".000Z"
    return datetime.strptime(s, ISO_FMT).replace(tzinfo=timezone.utc)
