from fastapi import APIRouter, HTTPException, Depends

from opspilot.models import Customer, Order
from opspilot.dependencies import get_order_service
from opspilot.services.orders import OrderService
from typing import Annotated
from fastapi import Depends

from opspilot.dependencies import get_customer_service
from opspilot.services.customers import CustomerService

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
CustomerServiceDep = Annotated[CustomerService, Depends(get_customer_service)]

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id:str, service: CustomerServiceDep)-> Customer:
    customer = service.get_customer(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    return customer

@router.get("/{customer_id}/orders", response_model=list[Order])
def get_customer_orders(customer_id: str, order_service: OrderServiceDep) -> list[Order]:
    return order_service.list_customer_orders(customer_id)