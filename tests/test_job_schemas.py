from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.db.models import JobRecord
from app.domain import JobStatus
from app.schemas import JobCreate, JobResponse, JobUpdate


def test_job_create_strips_input_and_uses_defaults() -> None:
    schema = JobCreate(company="  OpenAI  ", position="  AI Engineer  ")

    assert schema.company == "OpenAI"
    assert schema.position == "AI Engineer"
    assert schema.description == ""
    assert schema.priority == 0


@pytest.mark.parametrize("field", ["company", "position"])
def test_job_create_rejects_blank_required_fields(field: str) -> None:
    payload = {"company": "OpenAI", "position": "AI Engineer"}
    payload[field] = "   "

    with pytest.raises(ValidationError):
        JobCreate.model_validate(payload)


def test_job_create_rejects_invalid_url_and_extra_fields() -> None:
    with pytest.raises(ValidationError):
        JobCreate(
            company="OpenAI",
            position="AI Engineer",
            url="example.com/jobs/1",
        )

    with pytest.raises(ValidationError):
        JobCreate.model_validate(
            {"company": "OpenAI", "position": "AI Engineer", "unknown": True}
        )


def test_job_update_keeps_only_provided_fields() -> None:
    update = JobUpdate(status=JobStatus.INTERVIEW, deadline=None)

    assert update.model_dump(exclude_unset=True) == {
        "status": JobStatus.INTERVIEW,
        "deadline": None,
    }


def test_job_update_rejects_invalid_status_and_priority() -> None:
    with pytest.raises(ValidationError):
        JobUpdate.model_validate({"status": "未知状态"})
    with pytest.raises(ValidationError):
        JobUpdate(priority=6)


def test_job_response_reads_sqlalchemy_record() -> None:
    now = datetime.now(timezone.utc)
    record = JobRecord(
        id=uuid4(),
        user_id=uuid4(),
        company="OpenAI",
        position="AI Engineer",
        description="Build AI systems",
        url="https://example.com/jobs/1",
        note="",
        status=JobStatus.INTERVIEW.value,
        priority=3,
        deadline=None,
        created_at=now,
        updated_at=now,
    )

    response = JobResponse.model_validate(record)
    serialized = response.model_dump(mode="json")

    assert response.company == record.company
    assert response.status is JobStatus.INTERVIEW
    assert serialized["id"] == str(record.id)
    assert serialized["status"] == "面试"
