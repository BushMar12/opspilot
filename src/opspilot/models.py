from pydantic import BaseModel, Field

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    account_status: str

class SupportTicketCreate(BaseModel):
    customer_id: str
    order_id: str | None = None
    subject: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)

class SupportTicket(BaseModel):
    ticket_id: str
    customer_id: str
    order_id: str | None = None
    subject: str
    description: str
    status: str
