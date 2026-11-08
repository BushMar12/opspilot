from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    account_status: str

    