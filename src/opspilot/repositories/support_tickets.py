from opspilot.models import SupportTicket

class SupportTicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[str, SupportTicket] = {}
    
    def save(self, ticket: SupportTicket) -> SupportTicket:
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str) -> SupportTicket | None:
        return self._tickets.get(ticket_id)

    def count(self) -> int:
        return len(self._tickets)