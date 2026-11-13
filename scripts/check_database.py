from sqlalchemy import text

from opspilot.db.database import engine


def main() -> None:
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT
                    current_user,
                    current_database(),
                    inet_server_port()
                """
            )
        )

        row = result.one()

        print(f"User: {row[0]}")
        print(f"Database: {row[1]}")
        print(f"Port: {row[2]}")

if __name__ == "__main__":
    main()