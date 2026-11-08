from fastapi.testclient import TestClient

from opspilot.main import app

client = TestClient(app)

def test_get_existing_customer() -> None:
    response = client.get("/customers/CUS-1827")

    assert response.status_code == 200
    assert response.json() == {
        "customer_id": "CUS-1827",
        "name": "Alex Morgan",
        "email": "alex@example.com",
        "account_status": "active",
    }

def test_get_missing_customer_returns_404() -> None:
    response = client.get("/customers/CUS-9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer CUS-9999 not found"
    }