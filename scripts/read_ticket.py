from opspilot.db.database import SessionLocal
from opspilot.repositories.support_tickets import PostgresSupportTicketRepository


def main() -> None:
    repository = PostgresSupportTicketRepository(session_factory=SessionLocal,)

    ticket = repository.get_by_id("TKT-0001")

    print(ticket)

if __name__ == "__main__":
    main()