from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from opspilot.db.database import SessionLocal
from opspilot.repositories.support_tickets import PostgresSupportTicketRepository, SupportTicketRepositoryProtocol

from opspilot.services.support_tickets import SupportTicketService
from opspilot.repositories.orders import OrderRepositoryProtocol, PostgresOrderRepository
from opspilot.services.orders import OrderService

def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

def get_support_ticket_repository(session: Annotated[Session, Depends(get_db)]) -> SupportTicketRepositoryProtocol:
    return PostgresSupportTicketRepository(session)

def get_support_ticket_service(
    repository: Annotated[
        SupportTicketRepositoryProtocol,
        Depends(get_support_ticket_repository)
    ]
) -> SupportTicketService:
    return SupportTicketService(repository)

def get_order_repository(session: Annotated[Session, Depends(get_db)]) -> OrderRepositoryProtocol:
    return PostgresOrderRepository(session)

def get_order_service(repository: Annotated[OrderRepositoryProtocol, Depends(get_order_repository)]) -> OrderService:
    return OrderService(repository)

