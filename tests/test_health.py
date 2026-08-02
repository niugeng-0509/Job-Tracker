from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"].startswith(
        "application/json"
    )


def test_health_rejects_post_method() -> None:
    response = client.post("/health")

    assert response.status_code == 405