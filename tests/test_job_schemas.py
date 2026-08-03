import pytest
from pydantic import ValidationError

from app.models import Job, JobStatus
from app.schemas import (
    JobCreate,
    JobResponse,
    JobUpdate,
)


def test_job_create_strips_input_and_uses_defaults() -> None:
    schema = JobCreate(
        company="  OpenAI  ",
        position="  AI Engineer  ",
    )

    assert schema.company == "OpenAI"
    assert schema.position == "AI Engineer"
    assert schema.url == ""
    assert schema.note == ""


@pytest.mark.parametrize(
    "field",
    [
        "company",
        "position",
    ],
)
def test_job_create_rejects_blank_required_fields(
    field: str,
) -> None:
    payload = {
        "company": "OpenAI",
        "position": "AI Engineer",
    }
    payload[field] = "   "

    with pytest.raises(ValidationError) as exc_info:
        JobCreate.model_validate(payload)

    assert exc_info.value.errors()[0]["loc"] == (
        field,
    )


def test_job_create_rejects_invalid_url() -> None:
    with pytest.raises(ValidationError) as exc_info:
        JobCreate(
            company="OpenAI",
            position="AI Engineer",
            url="example.com/jobs/1",
        )

    assert exc_info.value.errors()[0]["loc"] == (
        "url",
    )


def test_job_schemas_accept_valid_url() -> None:
    valid_url = "https://example.com/jobs/1"

    create = JobCreate(
        company="OpenAI",
        position="AI Engineer",
        url=valid_url,
    )
    update = JobUpdate(
        url=valid_url,
    )

    assert create.url == valid_url
    assert update.url == valid_url


def test_job_create_rejects_extra_fields() -> None:
    payload = {
        "company": "OpenAI",
        "position": "AI Engineer",
        "priority": 100,
    }

    with pytest.raises(ValidationError) as exc_info:
        JobCreate.model_validate(payload)

    assert (
        exc_info.value.errors()[0]["type"]
        == "extra_forbidden"
    )


def test_job_update_keeps_only_provided_fields() -> None:
    update = JobUpdate(
        status=JobStatus.INTERVIEW,
    )

    assert update.model_dump(
        exclude_unset=True
    ) == {
        "status": JobStatus.INTERVIEW,
    }


def test_job_update_rejects_empty_payload() -> None:
    with pytest.raises(
        ValidationError,
        match="至少提供一个需要更新的字段",
    ):
        JobUpdate()


@pytest.mark.parametrize(
    "field",
    [
        "company",
        "status",
    ],
)
def test_job_update_rejects_explicit_null(
    field: str,
) -> None:
    with pytest.raises(
        ValidationError,
        match="更新字段不能为 null",
    ):
        JobUpdate.model_validate(
            {field: None}
        )


def test_job_update_allows_clearing_url_and_note() -> None:
    update = JobUpdate(
        url="",
        note="   ",
    )

    assert update.model_dump(
        exclude_unset=True
    ) == {
        "url": "",
        "note": "",
    }


def test_job_update_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError) as exc_info:
        JobUpdate.model_validate(
            {"status": "未知状态"}
        )

    assert exc_info.value.errors()[0]["loc"] == (
        "status",
    )


def test_job_response_reads_domain_job() -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
        status=JobStatus.INTERVIEW,
    )

    response = JobResponse.model_validate(job)
    serialized = response.model_dump(
        mode="json"
    )

    assert str(response.id) == job.id
    assert response.company == job.company
    assert response.created_at == job.created_at
    assert serialized["status"] == "面试"
    assert serialized["id"] == job.id
