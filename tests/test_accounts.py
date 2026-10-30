import pytest

from service.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db"), "API_TOKEN": "test-token"})
    return app.test_client()


HEADERS = {"Authorization": "Bearer test-token"}


def test_health_and_auth(client):
    assert client.get("/health").json == {"status": "ok"}
    assert client.get("/accounts").status_code == 401


def test_account_lifecycle(client):
    response = client.post("/accounts", json={"name": "Ada", "email": "Ada@Example.com"}, headers=HEADERS)
    assert response.status_code == 201
    account_id = response.json["id"]
    assert response.json["email"] == "ada@example.com"
    assert len(client.get("/accounts", headers=HEADERS).json) == 1
    assert client.get(f"/accounts/{account_id}", headers=HEADERS).json["name"] == "Ada"
    response = client.put(f"/accounts/{account_id}", json={"balance": 10.5, "active": False}, headers=HEADERS)
    assert response.json["balance"] == 10.5
    assert response.json["active"] is False
    assert client.delete(f"/accounts/{account_id}", headers=HEADERS).status_code == 204
    assert client.get(f"/accounts/{account_id}", headers=HEADERS).status_code == 404


def test_validation_and_duplicate(client):
    assert client.post("/accounts", json={}, headers=HEADERS).status_code == 400
    payload = {"name": "Ada", "email": "ada@example.com"}
    assert client.post("/accounts", json=payload, headers=HEADERS).status_code == 201
    assert client.post("/accounts", json=payload, headers=HEADERS).status_code == 409
    assert client.put("/accounts/1", json={"balance": -1}, headers=HEADERS).status_code == 400
