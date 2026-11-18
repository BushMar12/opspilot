from opspilot.models import Order
from opspilot.repositories.orders import OrderRepositoryProtocol

class OrderService:
    def __init__(self, repository: OrderRepositoryProtocol) -> None:
        self._repository = repository
    
    def get_order(self, order_id: str) -> Order | None:
        return self._repository.get_by_id(order_id)

    def list_customer_orders(self, customer_id: str) -> list[Order]:
        return self._repository.list_by_customer_id(customer_id)

