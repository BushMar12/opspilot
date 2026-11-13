from opspilot.db.base import Base
from opspilot.db.database import engine
from opspilot.db import tables

def main() -> None:
    Base.metadata.create_all(engine)

    print("Database tables created successfully.")

if __name__ == "__main__":
    main()