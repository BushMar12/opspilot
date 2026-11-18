from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from opspilot.dependencies import get_order_service
from opspilot.models import Order
from opspilot.services.orders import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str, service: OrderServiceDep) -> Order:
    order = service.get_order(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found"
        )
    
    return order