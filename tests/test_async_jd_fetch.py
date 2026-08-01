import asyncio

import pytest

from app.exceptions import ValidationError
from app.models import Job
from examples.async_jd_fetch import (
    fetch_concurrently,
    fetch_job_description,
)


def test_fetch_job_description_returns_content() -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
    )

    result = asyncio.run(
        fetch_job_description(
            job,
            delay_seconds=0,
        )
    )

    assert "OpenAI" in result
    assert "AI Engineer" in result
    assert job.url in result


def test_concurrent_fetch_preserves_job_order() -> None:
    jobs = [
        Job(
            company="OpenAI",
            position="AI Engineer",
            url="https://example.com/jobs/1",
        ),
        Job(
            company="Anthropic",
            position="Backend Engineer",
            url="https://example.com/jobs/2",
        ),
    ]

    results = asyncio.run(
        fetch_concurrently(
            jobs,
            delay_seconds=0,
        )
    )

    assert "OpenAI" in results[0]
    assert "Anthropic" in results[1]


def test_fetch_rejects_job_without_url() -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
    )

    with pytest.raises(
        ValidationError,
        match="获取 JD 需要招聘链接",
    ):
        asyncio.run(
            fetch_job_description(
                job,
                delay_seconds=0,
            )
        )


def test_fetch_rejects_negative_delay() -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
    )

    with pytest.raises(
        ValueError,
        match="等待时间不能为负数",
    ):
        asyncio.run(
            fetch_job_description(
                job,
                delay_seconds=-1,
            )
        )