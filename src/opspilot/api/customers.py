from fastapi import APIRouter, HTTPException

from opspilot.models import Customer

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

customers = {
    "CUS-1827": {
        "customer_id": "CUS-1827",
        "name": "Alex Morgan",
        "email": "alex@example.com",
        "account_status": "active",
    },
    "CUS-2001": {
        "customer_id": "CUS-2001",
        "name": "Jamie Lee",
        "email": "jamie@example.com",
        "account_status": "active",
    },
}

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id:str)-> Customer:
    customer = customers.get(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    return Customer(**customer)