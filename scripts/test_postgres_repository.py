from opspilot.db.database import SessionLocal
from opspilot.models import SupportTicketCreate
from opspilot.repositories.support_tickets import PostgresSupportTicketRepository
from opspilot.services.support_tickets import SupportTicketService

def main() -> None:
    repository = PostgresSupportTicketRepository(SessionLocal)
    service = SupportTicketService(repository)

    ticket = service.create_ticket(SupportTicketCreate(
        customer_id="CUS-1827",
        subject="Database persistence test",
        description="This ticket should remain after the Python process stops.",
        )
    )

    print("Created:")
    print(ticket)

    retrieved = service.get_ticket(ticket.ticket_id)

    print()
    print("Retrieved:")
    print(retrieved)

if __name__ == "__main__":
    main()