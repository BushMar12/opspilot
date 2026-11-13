from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from opspilot.db.database import SessionLocal
from opspilot.repositories.support_tickets import PostgresSupportTicketRepository, SupportTicketRepositoryProtocol

from opspilot.services.support_tickets import SupportTicketService

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