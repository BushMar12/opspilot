from datetime import datetime, timezone
from decimal import Decimal

from opspilot.db.database import SessionLocal
from opspilot.db.tables import CustomerRow, OrderRow

def main() -> None:
    with SessionLocal() as session:
        existing_customer = session.get(CustomerRow, "CUS-1827")

        if existing_customer is None:
            session.add(
                CustomerRow(
                    customer_id="CUS-1827",
                    name="Alex Morgan",
                    email="alex@example.com",
                    account_status='active',
                    created_at=datetime.now(timezone.utc),
                )
            )
            
        customer_2 = session.get(CustomerRow, "CUS-2001")

        if customer_2 is None:
            session.add(
                CustomerRow(
                    customer_id="CUS-2001",
                    name="Jamie Lee",
                    email="jamie@example.com",
                    account_status='active',
                    created_at=datetime.now(timezone.utc),
                )
            )
        
        order_1 = session.get(OrderRow, "ORD-8291")

        if order_1 is None:
            session.add(
                OrderRow(
                    order_id="ORD-8291",
                    customer_id="CUS-1827",
                    status="delivered",
                    order_date=datetime(2026, 10, 20, tzinfo=timezone.utc),
                    delivery_date=datetime(2026, 10, 24, tzinfo=timezone.utc),
                    total_amount=Decimal("149.95")
                )
            )
        
        order_2 = session.get(OrderRow, "ORD-9001")

        if order_2 is None:
            session.add(
                OrderRow(
                    order_id="ORD-9001",
                    customer_id="CUS-2001",
                    status="delivered",
                    order_date=datetime(2026, 10, 15, tzinfo=timezone.utc),
                    delivery_date=datetime(2026, 10, 19, tzinfo=timezone.utc),
                    total_amount=Decimal("799.99")
                )
            )

        session.commit()

if __name__ == "__main__":
    main()