from opspilot.models import Customer
from opspilot.repositories.customers import CustomerRepositoryProtocol

class CustomerService:
    def __init__(self, repository: CustomerRepositoryProtocol) -> None:
        self._repository = repository

    def get_customer(self, customer_id: str) -> Customer | None:
        return self._repository.get_by_id(customer_id)