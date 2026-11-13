from datetime import datetime, timezone
from opspilot.models import SupportTicket
from opspilot.repositories.support_tickets import InMemorySupportTicketRepository

def test_repository_saves_and_retrieves_ticket() -> None:
    repository = InMemorySupportTicketRepository()

    ticket = SupportTicket(
        ticket_id="TKT-0001",
        customer_id="CUS-1827",
        order_id=None,
        subject="Account issue",
        description="The customer cannot access the account portal.",
        status="open",
        created_at=datetime.now(timezone.utc)
    )

    repository.save(ticket)

    result = repository.get_by_id("TKT-0001")

    assert result == ticket

def test_repository_returns_none_for_missing_ticket() -> None:
    repository = InMemorySupportTicketRepository()

    result = repository.get_by_id("TKT-9999")

    assert result is None