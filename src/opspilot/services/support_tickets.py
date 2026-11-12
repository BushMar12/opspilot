from opspilot.models import SupportTicket, SupportTicketCreate
from opspilot.repositories.support_tickets import SupportTicketRepository

class SupportTicketService:
    def __init__(self, repository: SupportTicketRepository) -> None:
        self._repository = repository

    def create_ticket(self, ticket_data: SupportTicketCreate) -> SupportTicket:
        ticket_id = f"TKT-{self._repository.count() + 1:04d}"

        ticket = SupportTicket(
            ticket_id=ticket_id,
            customer_id=ticket_data.customer_id,
            order_id=ticket_data.order_id,
            subject=ticket_data.subject,
            description=ticket_data.description,
            status="open",
        )

        return self._repository.save(ticket)

    def get_ticket(self, ticket_id: str) -> SupportTicket | None:
        return self._repository.get_by_id(ticket_id)

    def resolve_ticket(self, ticket_id: str) -> SupportTicket | None:
        ticket = self._repository.get_by_id(ticket_id)

        if ticket is None:
            return None

        if ticket.status not in {"open", "in_progress"}:
            raise ValueError(f"Cannot resolve ticket in state {ticket.status}")
            
        ticket.status = "resolved"

        return self._repository.save(ticket)