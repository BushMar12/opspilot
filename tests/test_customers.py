import pytest
from fastapi.testclient import TestClient

from opspilot.dependencies import get_customer_service
from opspilot.main import app
from opspilot.models import Customer
from opspilot.repositories.customers import InMemoryCustomerRepository
from opspilot.services.customers import CustomerService


@pytest.fixture
def client() -> TestClient:
    repository = InMemoryCustomerRepository(
            customers=[
                Customer(
                    customer_id="CUS-1827",
                    name="Alex Morgan",
                    email="alex@example.com",
                    account_status="active",
            )
        ]
    )

    service = CustomerService(
        repository=repository
    )

    app.dependency_overrides[
        get_customer_service
    ] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()