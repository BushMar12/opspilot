from opspilot.models import SupportTicketCreate
from opspilot.services.support_tickets import SupportTicketService

def test_service_creates_open_ticket() -> None:
    service = SupportTicketService()

    ticket_data = SupportTicketCreate(
        customer_id="CUS-1827",
        subject="Account issue",
        description="The customer cannot access the account portal.",
    )

    ticket = service.create_ticket(ticket_data)
    assert ticket.customer_id == "CUS-1827"
    assert ticket.subject == "Account issue"
    assert ticket.ticket_id == "TKT-0001"

def test_service_can_retrieve_created_ticket() -> None:
    service = SupportTicketService()

    ticket_data = SupportTicketCreate(
        customer_id="CUS-1827",
        subject="Account issue",
        description="The customer cannot access the account portal.",
    )

    created_ticket = service.create_ticket(ticket_data)

    retrieved_ticket = service.get_ticket(created_ticket.ticket_id)
    assert retrieved_ticket == created_ticket

def test_service_returns_none_for_missing_ticket() -> None:
    service = SupportTicketService()

    result = service.get_ticket("TKT-9999")

    assert result is None

def test_service_resolves_ticket() -> None:
    service = SupportTicketService()

    ticket = service.create_ticket(
        SupportTicketCreate(
            customer_id="CUS-1827",
            subject="Account issue",
            description="The customer cannot access the account portal.",
        )
    )

    resolved_ticket = service.resolve_ticket(
        ticket.ticket_id
    )

    assert resolved_ticket is not None
    assert resolved_ticket.status == "resolved"