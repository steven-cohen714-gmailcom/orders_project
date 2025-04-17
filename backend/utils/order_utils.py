import re
from typing import Any, List
from datetime import datetime

def generate_order_number(current_number: str) -> str:
    """
    Generate the next order number by splitting off any non‑digit
    prefix (which can now be empty) and incrementing the numeric suffix,
    preserving zero‑padding.
    e.g. URC0001 → URC0002, PO009 → PO010, 0001 → 0002
    """
    m = re.match(r"^(\D*)(\d+)$", current_number)
    if not m:
        # if it doesn't end with digits, just append "1"
        return current_number + "1"
    prefix, digits = m.groups()
    width = len(digits)
    num = int(digits) + 1
    return f"{prefix}{str(num).zfill(width)}"


def determine_status(total: float, auth_threshold: float) -> str:
    """Return 'Awaiting Authorisation' if total > threshold, else 'Pending'."""
    return "Awaiting Authorisation" if total > auth_threshold else "Pending"


def validate_order_items(items: List[Any]) -> bool:
    """
    Ensure at least one item; qty > 0; price >= 0.
    Raises ValueError on violation.
    """
    if not items:
        raise ValueError("Order must contain at least one item")
    for item in items:
        if item.qty_ordered <= 0:
            raise ValueError("Quantity ordered must be greater than 0")
        if item.price < 0:
            raise ValueError("Price cannot be negative")
    return True
