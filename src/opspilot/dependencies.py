from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from opspilot.db.database import SessionLocal
from opspilot.repositories.support_tickets import PostgresSupportTicketRepository, SupportTicketRepositoryProtocol

from opspilot.services.support_tickets import SupportTicketService
from opspilot.repositories.orders import OrderRepositoryProtocol, PostgresOrderRepository
from opspilot.services.orders import OrderService

from opspilot.repositories.customers import CustomerRepositoryProtocol, PostgresCustomerRepository
from opspilot.services.customers import CustomerService

def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

def get_support_ticket_repository(session: Annotated[Session, Depends(get_db)]) -> SupportTicketRepositoryProtocol:
    return PostgresSupportTicketRepository(session)

def get_order_repository(session: Annotated[Session, Depends(get_db)]) -> OrderRepositoryProtocol:
    return PostgresOrderRepository(session)

def get_order_service(repository: Annotated[OrderRepositoryProtocol, Depends(get_order_repository)]) -> OrderService:
    return OrderService(repository)

def get_customer_repository(session: Annotated[Session, Depends(get_db)]) -> CustomerRepositoryProtocol:
    return PostgresCustomerRepository(session)

def get_customer_service(repository: Annotated[CustomerRepositoryProtocol, Depends(get_customer_repository)]) -> CustomerService:
    return CustomerService(repository)

def get_support_ticket_service(
    ticket_repository: Annotated[
        SupportTicketRepositoryProtocol,
        Depends(get_support_ticket_repository),
    ],
    customer_repository: Annotated[
        CustomerRepositoryProtocol,
        Depends(get_customer_repository)
    ],
    order_repository: Annotated[
        OrderRepositoryProtocol,
        Depends(get_order_repository)
    ],
) -> SupportTicketService:
    return SupportTicketService(
        repository=ticket_repository,
        customer_repository=(
            customer_repository
        ),
        order_repository=order_repository,
    )



