# File: /Users/stevencohen/Projects/universal_recycling/orders_project/backend/utils/order_utils.py
"""
Utility functions for Universal Recycling Purchase Order System
"""

def normalize_order_number(order_number: str) -> str:
    """
    Normalize order numbers to a consistent format (e.g., URC0001).
    """
    # Original logic:
    # prefix = "URC"
    # if not order_number.startswith(prefix):
    #     order_number = f"{prefix}{order_number}"
    
    # New logic to handle numbers without a prefix
    numeric = ''.join(filter(str.isdigit, order_number))
    try:
        num = int(numeric)
        return f"{num:04d}"  # Ensures 4 digits, e.g., 0001
    except ValueError:
        raise ValueError(f"Order number must end with a number, got: {order_number}")

def calculate_order_total(items: list) -> float:
    """
    Calculate the total cost of an order based on its items.
    
    Args:
        items (list): List of order items, where each item is a dict with 'qty_ordered' and 'price' keys.
    
    Returns:
        float: The total cost of the order.
    
    Raises:
        KeyError: If an item is missing 'qty_ordered' or 'price'.
    """
    total = 0.0
    for item in items:
        qty = item["qty_ordered"]
        price = item["price"]
        total += qty * price
    return total