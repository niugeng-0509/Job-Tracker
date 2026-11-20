from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings, get_settings
from app.db.session import Base, get_session
from app.main import app


@pytest.fixture
def api_client(tmp_path: Path) -> Iterator[TestClient]:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    testing_session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    settings = Settings(
        database_url=str(engine.url),
        jwt_secret="test-secret-that-is-not-used-in-production",
        upload_dir=tmp_path / "uploads",
    )

    def override_session() -> Iterator[Session]:
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_settings] = lambda: settings
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
        engine.dispose()


def auth_headers(client: TestClient, email: str = "user@example.com") -> dict[str, str]:
    register = client.post("/auth/register", json={"email": email, "password": "strong-pass-123"})
    assert register.status_code == 201
    login = client.post("/auth/login", data={"username": email, "password": "strong-pass-123"})
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_auth_rejects_duplicate_and_bad_credentials(api_client: TestClient) -> None:
    auth_headers(api_client)
    duplicate = api_client.post("/auth/register", json={"email": "user@example.com", "password": "strong-pass-123"})
    bad_login = api_client.post("/auth/login", data={"username": "user@example.com", "password": "wrong-password"})
    assert duplicate.status_code == 409
    assert bad_login.status_code == 401
    assert api_client.get("/jobs").status_code == 401
    assert api_client.get("/jobs", headers={"Authorization": "Bearer broken"}).status_code == 401


def test_job_crud_pagination_filter_and_validation(api_client: TestClient) -> None:
    headers = auth_headers(api_client)
    first = api_client.post("/jobs", headers=headers, json={"company": "OpenAI", "position": "AI Engineer", "priority": 5})
    second = api_client.post("/jobs", headers=headers, json={"company": "Anthropic", "position": "Research Engineer"})
    assert first.status_code == second.status_code == 201
    duplicate = api_client.post("/jobs", headers=headers, json={"company": "OpenAI", "position": "AI Engineer"})
    assert duplicate.status_code == 409
    invalid_url = api_client.post("/jobs", headers=headers, json={"company": "Bad", "position": "URL", "url": "example.com"})
    assert invalid_url.status_code == 422
    page = api_client.get("/jobs?page=1&page_size=1&keyword=Open&sort_by=priority", headers=headers).json()
    assert page["total"] == 1
    assert page["items"][0]["company"] == "OpenAI"
    job_id = first.json()["id"]
    updated = api_client.patch(f"/jobs/{job_id}", headers=headers, json={"status": "面试", "note": "prepare"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "面试"
    assert api_client.patch(f"/jobs/{job_id}", headers=headers, json={}).status_code == 422
    assert api_client.get("/jobs/not-a-uuid", headers=headers).status_code == 422
    assert api_client.delete(f"/jobs/{job_id}", headers=headers).status_code == 204
    assert api_client.get(f"/jobs/{job_id}", headers=headers).status_code == 404


def test_users_cannot_discover_each_others_jobs(api_client: TestClient) -> None:
    first_headers = auth_headers(api_client, "first@example.com")
    second_headers = auth_headers(api_client, "second@example.com")
    job = api_client.post("/jobs", headers=first_headers, json={"company": "Private", "position": "Role"}).json()
    assert api_client.get(f"/jobs/{job['id']}", headers=second_headers).status_code == 404
    assert api_client.patch(f"/jobs/{job['id']}", headers=second_headers, json={"note": "steal"}).status_code == 404
    assert api_client.delete(f"/jobs/{job['id']}", headers=second_headers).status_code == 404
    assert api_client.get("/jobs", headers=second_headers).json()["items"] == []


def test_events_and_tasks_are_owned(api_client: TestClient) -> None:
    headers = auth_headers(api_client)
    job = api_client.post("/jobs", headers=headers, json={"company": "OpenAI", "position": "Engineer"}).json()
    event = api_client.post(f"/jobs/{job['id']}/events", headers=headers, json={"event_type": "interview", "note": "round 1"})
    task = api_client.post("/tasks", headers=headers, json={"title": "Prepare", "job_id": job["id"]})
    assert event.status_code == task.status_code == 201
    assert len(api_client.get(f"/jobs/{job['id']}/events", headers=headers).json()) == 1
    patched = api_client.patch(f"/tasks/{task.json()['id']}", headers=headers, json={"completed": True})
    assert patched.json()["completed"] is True
    assert len(api_client.get("/tasks?completed=true", headers=headers).json()) == 1
    other_headers = auth_headers(api_client, "other@example.com")
    assert api_client.get(f"/jobs/{job['id']}/events", headers=other_headers).status_code == 404
    assert api_client.patch(f"/tasks/{task.json()['id']}", headers=other_headers, json={"completed": False}).status_code == 404


def test_document_upload_limits_and_delete(api_client: TestClient) -> None:
    headers = auth_headers(api_client)
    bad = api_client.post("/documents", headers=headers, data={"document_type": "resume"}, files={"file": ("x.png", b"png", "image/png")})
    assert bad.status_code == 415
    fake_pdf = api_client.post("/documents", headers=headers, data={"document_type": "resume"}, files={"file": ("x.pdf", b"not pdf", "application/pdf")})
    assert fake_pdf.status_code == 415
    created = api_client.post("/documents", headers=headers, data={"document_type": "resume"}, files={"file": ("resume.txt", b"hello", "text/plain")})
    assert created.status_code == 201
    assert api_client.get("/documents", headers=headers).json()[0]["filename"] == "resume.txt"
    assert api_client.delete(f"/documents/{created.json()['id']}", headers=headers).status_code == 204
    assert api_client.get("/documents", headers=headers).json() == []
