from opspilot.models import SupportTicket, SupportTicketCreate

class SupportTicketService:
    def __init__(self) -> None:
        self._tickets: dict[str, SupportTicket] = {}

    def create_ticket(self, ticket_data: SupportTicketCreate) -> SupportTicket:
        ticket_id = f"TKT-{len(self._tickets) + 1:04d}"

        ticket = SupportTicket(
            ticket_id=ticket_id,
            customer_id=ticket_data.customer_id,
            order_id=ticket_data.order_id,
            subject=ticket_data.subject,
            description=ticket_data.description,
            status="open",
        )

        self._tickets[ticket_id] = ticket

        return ticket

    def get_ticket(self, ticket_id: str) -> SupportTicket | None:
        return self._tickets.get(ticket_id)