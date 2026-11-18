from typing import Protocol

from sqlalchemy.orm import Session
from sqlalchemy import select

from opspilot.db.tables import OrderRow
from opspilot.models import Order

class OrderRepositoryProtocol(Protocol):
    def get_by_id(self, order_id: str) -> Order | None:
        ...

    def list_by_customer_id(self, customer_id: str) -> list[Order]:
        ...

class PostgresOrderRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, order_id: str) -> Order | None:
        row = self._session.get(OrderRow, order_id)

        if row is None:
            return None
        
        return self._to_model(row)

    def list_by_customer_id(self, customer_id: str) -> list[Order]:
        statement = select(OrderRow).where(OrderRow.customer_id == customer_id).order_by(OrderRow.order_date.desc())

        rows = self._session.scalars(statement).all()

        return [self._to_model(row) for row in rows]

    @staticmethod
    def _to_model(row: OrderRow) -> Order:
        return Order(
            order_id=row.order_id,
            customer_id=row.customer_id,
            status=row.status,
            order_date=row.order_date,
            delivery_date=row.delivery_date,
            total_amount=row.total_amount
        )
    
class InMemoryOrderRepository:
    def __init__(self, orders: list[Order] | None = None) -> None:
        self._orders = {order.order_id: order for order in (orders or [])}

    def get_by_id(self, order_id:str) -> Order | None:
        return self._orders.get(order_id)

    def list_by_customer_id(self, customer_id: str) -> list[Order]:
        return [order for order in self._orders.values() if customer_id == order.customer_id]
        