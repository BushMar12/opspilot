from datetime import datetime, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from opspilot.dependencies import get_support_ticket_service
from opspilot.main import app
from opspilot.models import Order, Customer
from opspilot.repositories.orders import InMemoryOrderRepository
from opspilot.repositories.customers import InMemoryCustomerRepository
from opspilot.repositories.support_tickets import InMemorySupportTicketRepository

from opspilot.services.support_tickets import SupportTicketService


@pytest.fixture
def client() -> TestClient:
    ticket_repository = InMemorySupportTicketRepository()
    customer_repository = InMemoryCustomerRepository(
        customers=[
            Customer(
                customer_id="CUS-1827",
                name="Alex Morgan",
                email="alex@example.com",
                account_status="active",
            )
        ]
    )

    order_repository = InMemoryOrderRepository(
        orders=[
            Order(
                order_id="ORD-8291",
                customer_id="CUS-1827",
                status="delivered",
                order_date=datetime(2026, 10, 20, 0, 0, 0, tzinfo=timezone.utc),
                delivery_date=datetime(2026, 10, 24, 0, 0, 0, tzinfo=timezone.utc),
                total_amount=Decimal("149.95"),
            )
        ]
    )

    service = SupportTicketService(
        repository=ticket_repository,
        customer_repository=customer_repository,
        order_repository=order_repository,
    )

    app.dependency_overrides[
        get_support_ticket_service
    ] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_create_support_ticket(client: TestClient) -> None:
    response = client.post(
        "/support-tickets",
        json={
            "customer_id": "CUS-1827",
            "order_id": "ORD-8291",
            "subject": "Damaged headphones",
            "description": "The headphones arrived cracked and do not turn on.",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["customer_id"] == "CUS-1827"
    assert body["order_id"] == "ORD-8291"
    assert body["subject"] == "Damaged headphones"
    assert body["status"] == "open"
    assert body["ticket_id"].startswith("TKT-")


def test_create_support_ticket_rejects_short_description(client: TestClient) -> None:
    response = client.post(
        "/support-tickets",
        json={
            "customer_id": "CUS-1827",
            "subject": "Damaged headphones",
            "description": "Too short",
        },
    )

    assert response.status_code == 422

def test_get_created_support_ticket(client: TestClient) -> None:
    create_response = client.post(
        "/support-tickets",
        json={
            "customer_id": "CUS-1827",
            "subject": "Account issue",
            "description": "The customer cannot access the account portal.",
        },
    )

    ticket_id = create_response.json()["ticket_id"]

    get_response = client.get(
        f"/support-tickets/{ticket_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["ticket_id"] == ticket_id