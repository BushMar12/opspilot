from typing import Protocol

from sqlalchemy.orm import Session

from opspilot.db.tables import CustomerRow
from opspilot.models import Customer


class CustomerRepositoryProtocol(Protocol):
    def get_by_id(self, customer_id: str) -> Customer | None:
        ...

class PostgresCustomerRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, customer_id: str) -> Customer | None:
        row = self._session.get(CustomerRow, customer_id)
        if row is None:
            return None
        return Customer(customer_id=row.customer_id, name=row.name, email=row.email, account_status=row.account_status)


class InMemoryCustomerRepository:
    def __init__(self, customers: list[Customer] | None = None) -> None:
        self._customers = {customer.customer_id: customer for customer in (customers or [])}

    def get_by_id(self, customer_id: str) -> Customer | None:
        return self._customers.get(customer_id)