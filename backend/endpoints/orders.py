from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3

from ..database import create_order, get_setting, update_setting
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items

router = APIRouter(prefix="/orders", tags=["orders"])

class OrderItem(BaseModel):
    item_code: str = Field(min_length=1)
    item_description: str = Field(min_length=1)
    project: str = Field(min_length=1)
    qty_ordered: float = Field(gt=0)
    price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.qty_ordered * self.price

class OrderCreate(BaseModel):
    order_number: Optional[str] = None
    requester: str = Field(min_length=1)
    items: List[OrderItem] = Field(min_length=1)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

@router.post("")
async def create_new_order(order: OrderCreate):
    """
    Create a new purchase order.
    Args:
        order: OrderCreate model containing order details and items
    Returns:
        Created order with items and status
    Raises:
        HTTPException: For database errors or validation failures
    """
    try:
        # Validate order items
        validate_order_items(order.items)

        # Calculate total
        total = order.total

        # Get settings
        auth_threshold = float(get_setting("auth_threshold"))
        current_order_number = get_setting("order_number_start")

        # Generate order number if not provided
        if not order.order_number:
            order.order_number = generate_order_number(current_order_number)
            # Generate the next order number and update settings
            next_order_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_order_number)

        # Determine status based on total
        status = determine_status(total, auth_threshold)

        # Prepare order data
        order_data = order.dict()
        order_data["status"] = status
        order_data["total"] = total

        # Create order and items in database
        result = create_order(
            order_data=order_data,
            items=[item.dict() for item in order.items]
        )

        # Format the date in response
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        return {
            "message": "Order created successfully",
            "order": result
        }

    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("")
async def get_orders(status: Optional[str] = None):
    """
    Retrieve all orders or filter by status.
    Args:
        status: Optional status filter (e.g., Pending, Authorised)
    Returns:
        List of orders
    Raises:
        HTTPException: For database errors
    """
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        query = "SELECT id, order_number, status, created_date, total, order_note, supplier_note, requester FROM orders"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        cursor.execute(query, params)
        orders = cursor.fetchall()
        conn.close()

        # Format response
        result = []
        for order in orders:
            result.append({
                "id": order[0],
                "order_number": order[1],
                "status": order[2],
                "created_date": datetime.fromisoformat(order[3]).strftime("%d/%m/%Y"),
                "total": order[4],
                "order_note": order[5],
                "supplier_note": order[6],
                "requester": order[7]
            })

        return {"orders": result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
