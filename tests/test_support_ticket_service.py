from datetime import datetime, timezone
from decimal import Decimal

import pytest

from opspilot.exceptions import (
    OrderCustomerMismatchError,
    OrderNotFoundError,
)
from opspilot.models import (
    Order,
    SupportTicketCreate,
)
from opspilot.repositories.orders import (
    InMemoryOrderRepository,
)
from opspilot.repositories.support_tickets import (
    InMemorySupportTicketRepository,
)
from opspilot.services.support_tickets import (
    SupportTicketService,
)


def create_order(
    order_id: str = "ORD-8291",
    customer_id: str = "CUS-1827",
) -> Order:
    return Order(
        order_id=order_id,
        customer_id=customer_id,
        status="delivered",
        order_date=datetime(
            2026,
            10,
            20,
            tzinfo=timezone.utc,
        ),
        delivery_date=datetime(
            2026,
            10,
            24,
            tzinfo=timezone.utc,
        ),
        total_amount=Decimal("149.95"),
    )


def create_service(
    orders: list[Order] | None = None,
) -> SupportTicketService:
    ticket_repository = (
        InMemorySupportTicketRepository()
    )

    order_repository = InMemoryOrderRepository(
        orders=orders or []
    )

    return SupportTicketService(
        repository=ticket_repository,
        order_repository=order_repository,
    )


def test_create_ticket_without_order() -> None:
    service = create_service()

    ticket_data = SupportTicketCreate(
        customer_id="CUS-1827",
        order_id=None,
        subject="Account access problem",
        description=(
            "The customer cannot access "
            "the account portal."
        ),
    )

    ticket = service.create_ticket(ticket_data)

    assert ticket.ticket_id == "TKT-0001"
    assert ticket.customer_id == "CUS-1827"
    assert ticket.order_id is None
    assert ticket.subject == "Account access problem"
    assert ticket.status == "open"
    assert ticket.created_at is not None


def test_create_ticket_with_valid_order() -> None:
    order = create_order()

    service = create_service(
        orders=[order]
    )

    ticket_data = SupportTicketCreate(
        customer_id="CUS-1827",
        order_id="ORD-8291",
        subject="Damaged headphones",
        description=(
            "The headphones arrived damaged "
            "during delivery."
        ),
    )

    ticket = service.create_ticket(ticket_data)

    assert ticket.ticket_id == "TKT-0001"
    assert ticket.customer_id == "CUS-1827"
    assert ticket.order_id == "ORD-8291"
    assert ticket.status == "open"


def test_get_existing_ticket() -> None:
    service = create_service()

    created_ticket = service.create_ticket(
        SupportTicketCreate(
            customer_id="CUS-1827",
            order_id=None,
            subject="Account access problem",
            description=(
                "The customer cannot access "
                "the account portal."
            ),
        )
    )

    result = service.get_ticket(
        created_ticket.ticket_id
    )

    assert result is not None
    assert (
        result.ticket_id
        == created_ticket.ticket_id
    )
    assert result.customer_id == "CUS-1827"


def test_get_missing_ticket_returns_none() -> None:
    service = create_service()

    result = service.get_ticket(
        "TKT-9999"
    )

    assert result is None


def test_resolve_open_ticket() -> None:
    service = create_service()

    created_ticket = service.create_ticket(
        SupportTicketCreate(
            customer_id="CUS-1827",
            order_id=None,
            subject="Account access problem",
            description=(
                "The customer cannot access "
                "the account portal."
            ),
        )
    )

    resolved_ticket = service.resolve_ticket(
        created_ticket.ticket_id
    )

    assert resolved_ticket is not None
    assert resolved_ticket.status == "resolved"


def test_resolve_missing_ticket_returns_none() -> None:
    service = create_service()

    result = service.resolve_ticket(
        "TKT-9999"
    )

    assert result is None


def test_cannot_resolve_already_resolved_ticket() -> None:
    service = create_service()

    created_ticket = service.create_ticket(
        SupportTicketCreate(
            customer_id="CUS-1827",
            order_id=None,
            subject="Account access problem",
            description=(
                "The customer cannot access "
                "the account portal."
            ),
        )
    )

    service.resolve_ticket(
        created_ticket.ticket_id
    )

    with pytest.raises(
        ValueError,
        match="Cannot resolve ticket",
    ):
        service.resolve_ticket(
            created_ticket.ticket_id
        )


def test_rejects_missing_order() -> None:
    service = create_service()

    ticket_data = SupportTicketCreate(
        customer_id="CUS-1827",
        order_id="ORD-9999",
        subject="Missing order",
        description=(
            "The customer is referencing "
            "an order that does not exist."
        ),
    )

    with pytest.raises(
        OrderNotFoundError,
        match="ORD-9999",
    ):
        service.create_ticket(
            ticket_data
        )


def test_rejects_order_owned_by_different_customer() -> None:
    order = create_order(
        order_id="ORD-9001",
        customer_id="CUS-2001",
    )

    service = create_service(
        orders=[order]
    )

    ticket_data = SupportTicketCreate(
        customer_id="CUS-1827",
        order_id="ORD-9001",
        subject="Incorrect customer order",
        description=(
            "This order belongs to "
            "a different customer."
        ),
    )

    with pytest.raises(
        OrderCustomerMismatchError,
        match="ORD-9001",
    ):
        service.create_ticket(
            ticket_data
        )


def test_multiple_tickets_get_different_ids() -> None:
    service = create_service()

    first_ticket = service.create_ticket(
        SupportTicketCreate(
            customer_id="CUS-1827",
            order_id=None,
            subject="First support issue",
            description=(
                "This is the first support "
                "ticket created in the test."
            ),
        )
    )

    second_ticket = service.create_ticket(
        SupportTicketCreate(
            customer_id="CUS-1827",
            order_id=None,
            subject="Second support issue",
            description=(
                "This is the second support "
                "ticket created in the test."
            ),
        )
    )

    assert first_ticket.ticket_id == "TKT-0001"
    assert second_ticket.ticket_id == "TKT-0002"