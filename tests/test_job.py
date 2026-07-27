from datetime import datetime, timezone
from uuid import UUID

import pytest

from app.exceptions import ValidationError
from app.models import Job, JobStatus


def test_create_job_with_explicit_values() -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
        note="Remote",
        status=JobStatus.INTERVIEW,
    )

    assert job.company == "OpenAI"
    assert job.position == "AI Engineer"
    assert job.url == "https://example.com/jobs/1"
    assert job.note == "Remote"
    assert job.status is JobStatus.INTERVIEW


def test_job_uses_expected_defaults() -> None:
    before_creation = datetime.now(timezone.utc)

    job = Job(
        company="OpenAI",
        position="Python Engineer",
    )

    after_creation = datetime.now(timezone.utc)

    assert job.url == ""
    assert job.note == ""
    assert job.status is JobStatus.PENDING

    assert str(UUID(job.id)) == job.id

    assert before_creation <= job.created_at <= after_creation
    assert before_creation <= job.updated_at <= after_creation
    assert job.created_at.tzinfo is timezone.utc
    assert job.updated_at.tzinfo is timezone.utc


def test_job_strips_surrounding_whitespace() -> None:
    job = Job(
        company="  OpenAI  ",
        position="\nAI Engineer\t",
        url="  https://example.com/jobs/1  ",
        note="  Remote position  ",
    )

    assert job.company == "OpenAI"
    assert job.position == "AI Engineer"
    assert job.url == "https://example.com/jobs/1"
    assert job.note == "Remote position"


def test_mark_updated_refreshes_updated_at() -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
    )
    old_time = datetime(
        year=2020,
        month=1,
        day=1,
        tzinfo=timezone.utc,
    )
    job.updated_at = old_time

    job.mark_updated()

    assert job.updated_at > old_time
    assert job.updated_at.tzinfo is timezone.utc


@pytest.mark.parametrize(
    "invalid_company",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_job_rejects_empty_company(
    invalid_company: str,
) -> None:
    with pytest.raises(
        ValidationError,
        match="公司名称不能为空",
    ):
        Job(
            company=invalid_company,
            position="AI Engineer",
        )


@pytest.mark.parametrize(
    "invalid_position",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_job_rejects_empty_position(
    invalid_position: str,
) -> None:
    with pytest.raises(
        ValidationError,
        match="岗位名称不能为空",
    ):
        Job(
            company="OpenAI",
            position=invalid_position,
        )


@pytest.mark.parametrize(
    "invalid_url",
    [
        "www.example.com/jobs/1",
        "example.com/jobs/1",
        "ftp://example.com/jobs/1",
    ],
)
def test_job_rejects_invalid_url(
    invalid_url: str,
) -> None:
    with pytest.raises(
        ValidationError,
        match="招聘链接必须以 http:// 或 https:// 开头",
    ):
        Job(
            company="OpenAI",
            position="AI Engineer",
            url=invalid_url,
        )


@pytest.mark.parametrize(
    "valid_url",
    [
        "http://example.com/jobs/1",
        "https://example.com/jobs/1",
    ],
)
def test_job_accepts_http_and_https_urls(
    valid_url: str,
) -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
        url=valid_url,
    )

    assert job.url == valid_url
