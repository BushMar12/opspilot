from typing import Protocol
from opspilot.models import SupportTicket

from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from opspilot.db.tables import SupportTicketRow

class InMemorySupportTicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[str, SupportTicket] = {}
    
    def save(self, ticket: SupportTicket) -> SupportTicket:
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str) -> SupportTicket | None:
        return self._tickets.get(ticket_id)

    def count(self) -> int:
        return len(self._tickets)

class SupportTicketRepositoryProtocol(Protocol):
    def save(self, ticket: SupportTicket) -> SupportTicket:
        ...

    def get_by_id(self, ticket_id: str) -> SupportTicket | None:
        ...

    def count(self) -> int:
        ...

class PostgresSupportTicketRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
    
    def save(self, ticket: SupportTicket) -> SupportTicket:
        with self._session_factory() as session:
            row = session.get(
                SupportTicketRow,
                ticket.ticket_id
            )

            if row is None:
                row = SupportTicketRow(
                    ticket_id=ticket.ticket_id,
                    customer_id=ticket.customer_id,
                    order_id=ticket.order_id,
                    subject=ticket.subject,
                    description=ticket.description,
                    status=ticket.status,
                    created_at=ticket.created_at,
                )

                session.add(row)

            else:
                row.customer_id = ticket.customer_id
                row.order_id = ticket.order_id
                row.subject = ticket.subject
                row.description = ticket.description
                row.status = ticket.status
                row.created_at = ticket.created_at

            session.commit()

        return ticket
    
    def get_by_id(self, ticket_id: str) -> SupportTicket | None:
        with self._session_factory() as session:
            row = session.get(SupportTicketRow, ticket_id)

            if row is None:
                return None
            
            return SupportTicket(
                ticket_id=row.ticket_id,
                customer_id=row.customer_id,
                order_id=row.order_id,
                subject=row.subject,
                description=row.description,
                status=row.status,
                created_at=row.created_at,
            )

    def count(self) -> int:
        with self._session_factory() as session:
            statement = select(func.count(SupportTicketRow.ticket_id))

            return session.scalar(statement) or 0