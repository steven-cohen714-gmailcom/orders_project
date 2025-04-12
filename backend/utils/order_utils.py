from typing import Dict, Any, List
from datetime import datetime

def generate_order_number(current_number: str) -> str:
    """
    Generate the next order number based on the current number.
    Args:
        current_number: Current order number from settings (e.g., "PO001")
    Returns:
        Next order number in sequence
    """
    # Extract the numeric part
    num = int(current_number[2:])
    # Generate new number with leading zeros
    return f"PO{str(num + 1).zfill(3)}"

def determine_status(total: float, auth_threshold: float) -> str:
    """
    Determine order status based on total amount and authorization threshold.
    Args:
        total: Order total amount
        auth_threshold: Authorization threshold from settings
    Returns:
        Status string: either "Pending" or "Awaiting Authorisation"
    """
    return "Awaiting Authorisation" if total > auth_threshold else "Pending"

def validate_order_items(items: List[Any]) -> bool:
    """
    Validate order items and their totals.
    Args:
        items: List of OrderItem objects
    Returns:
        True if valid, raises ValueError if invalid
    """
    if not items:
        raise ValueError("Order must contain at least one item")
    
    for item in items:
        if item.qty_ordered <= 0:
            raise ValueError("Quantity ordered must be greater than 0")
        if item.price < 0:
            raise ValueError("Price cannot be negative")
    
    return True
