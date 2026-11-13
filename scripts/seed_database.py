from datetime import datetime, timezone

from opspilot.db.database import SessionLocal
from opspilot.db.tables import CustomerRow

def main() -> None:
    with SessionLocal() as session:
        existing_customer = session.get(
            CustomerRow,
            "CUS-1827",
        )

        if existing_customer is not None:
            print("Customer CUS-1827 already exists.")
            return

        customer = CustomerRow(
            customer_id="CUS-1827",
            name="Alex Morgan",
            email="alex@example.com",
            account_status='active',
            created_at=datetime.now(timezone.utc),
        )

        session.add(customer)
        session.commit()

        print("Customer CUS-1827 created")

if __name__ == "__main__":
    main()