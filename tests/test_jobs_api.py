from collections.abc import Iterator
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_job_service
from app.api.main import app
from app.models import JobStatus
from app.repositories import JsonJobRepository
from app.services import JobService


@pytest.fixture
def api_client(
    tmp_path: Path,
) -> Iterator[TestClient]:
    data_file = tmp_path / "jobs.json"
    repository = JsonJobRepository(data_file)
    service = JobService(repository)

    def override_job_service() -> JobService:
        return service

    app.dependency_overrides[
        get_job_service
    ] = override_job_service

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(
            get_job_service,
            None,
        )


def test_create_job_returns_201(
    api_client: TestClient,
) -> None:
    response = api_client.post(
        "/jobs",
        json={
            "company": "OpenAI",
            "position": "AI Engineer",
            "url": "https://example.com/jobs/1",
            "note": "Remote",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert str(UUID(str(body["id"]))) == body["id"]
    assert body["company"] == "OpenAI"
    assert body["position"] == "AI Engineer"
    assert body["url"] == "https://example.com/jobs/1"
    assert body["note"] == "Remote"
    assert body["status"] == JobStatus.PENDING.value
    assert "created_at" in body
    assert "updated_at" in body


@pytest.mark.parametrize(
    "payload",
    [
        {
            "company": "OpenAI",
        },
        {
            "company": "OpenAI",
            "position": "AI Engineer",
            "url": "example.com/jobs/1",
        },
    ],
)
def test_create_job_rejects_invalid_payload(
    api_client: TestClient,
    payload: dict[str, object],
) -> None:
    response = api_client.post(
        "/jobs",
        json=payload,
    )

    assert response.status_code == 422


def test_create_job_rejects_duplicate(
    api_client: TestClient,
) -> None:
    payload = {
        "company": "OpenAI",
        "position": "AI Engineer",
        "url": "https://example.com/jobs/1",
    }

    first_response = api_client.post(
        "/jobs",
        json=payload,
    )
    second_response = api_client.post(
        "/jobs",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": (
            "该岗位可能重复："
            "OpenAI - AI Engineer"
        ),
    }
