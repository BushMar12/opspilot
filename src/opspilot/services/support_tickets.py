from datetime import datetime, timezone

from opspilot.models import SupportTicket, SupportTicketCreate
from opspilot.repositories.support_tickets import SupportTicketRepositoryProtocol
from opspilot.repositories.orders import OrderRepositoryProtocol
from opspilot.exceptions import OrderNotFoundError, OrderCustomerMismatchError, CustomerNotFoundError

from opspilot.repositories.customers import CustomerRepositoryProtocol

from uuid import uuid4

class SupportTicketService:
    def __init__(self, repository: SupportTicketRepositoryProtocol, customer_repository: CustomerRepositoryProtocol, order_repository: OrderRepositoryProtocol) -> None:
        self._repository = repository
        self._order_repository = order_repository
        self._customer_repository = customer_repository

    def create_ticket(self, ticket_data: SupportTicketCreate) -> SupportTicket:
        customer = self._customer_repository.get_by_id(ticket_data.customer_id)

        if customer is None:
            raise CustomerNotFoundError(f"Customer {ticket_data.customer_id} not found")
            
        if ticket_data.order_id is not None:
            order = self._order_repository.get_by_id(ticket_data.order_id)

            if order is None:
                raise OrderNotFoundError(f"Order {ticket_data.order_id} not found")

            if order.customer_id != ticket_data.customer_id:
                raise OrderCustomerMismatchError(f"Order {ticket_data.order_id} does not belong to customer {ticket_data.customer_id}")

        ticket_id = f"TKT-{uuid4()}"

        ticket = SupportTicket(
            ticket_id=ticket_id,
            customer_id=ticket_data.customer_id,
            order_id=ticket_data.order_id,
            subject=ticket_data.subject,
            description=ticket_data.description,
            status="open",
            created_at=datetime.now(timezone.utc)
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