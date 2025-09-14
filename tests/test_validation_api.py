import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from fastapi.testclient import TestClient
from src.api.main import app, validation_service, get_db


class DummyDB:
    def add(self, obj):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


def override_get_db():
    db = DummyDB()
    try:
        yield db
    finally:
        pass


def test_validate_uses_validation_service(monkeypatch):
    calls = {"ein": False, "duns": False}

    async def mock_validate_ein(ein):
        calls["ein"] = True
        return True

    async def mock_validate_duns(duns):
        calls["duns"] = True
        return False

    monkeypatch.setattr(validation_service, "validate_ein", mock_validate_ein)
    monkeypatch.setattr(validation_service, "validate_duns", mock_validate_duns)

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    response = client.post("/validate", json={"ein": "12-3456789", "duns": "12-345-6789"})

    assert response.status_code == 200
    assert response.json() == {
        "valid": False,
        "details": {"ein": True, "duns": False},
    }
    assert calls["ein"] and calls["duns"]

    app.dependency_overrides.clear()
