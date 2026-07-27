import pytest

from app.exceptions import JobNotFoundError, ValidationError
from app.models import Job, JobStatus
from app.services import JobService


class FakeJobRepository:
    """只在内存中保存岗位，不操作真实 JSON 文件。"""

    def __init__(self) -> None:
        self.jobs: list[Job] = []

    def get_all(self) -> list[Job]:
        return list(self.jobs)

    def get_by_id(self, job_id: str) -> Job:
        for job in self.jobs:
            if job.id == job_id:
                return job

        raise JobNotFoundError(
            f"没有找到岗位：{job_id}"
        )

    def save(self, job: Job) -> Job:
        self.jobs.append(job)
        return job

    def update(self, job: Job) -> Job:
        for index, existing_job in enumerate(self.jobs):
            if existing_job.id == job.id:
                self.jobs[index] = job
                return job

        raise JobNotFoundError(
            f"没有找到岗位：{job.id}"
        )

    def delete(self, job_id: str) -> Job:
        for index, job in enumerate(self.jobs):
            if job.id == job_id:
                return self.jobs.pop(index)

        raise JobNotFoundError(
            f"没有找到岗位：{job_id}"
        )


@pytest.fixture
def repository() -> FakeJobRepository:
    return FakeJobRepository()


@pytest.fixture
def service(
    repository: FakeJobRepository,
) -> JobService:
    return JobService(repository)


def test_add_job_saves_job(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    job = service.add_job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
    )

    assert job.company == "OpenAI"
    assert job.position == "AI Engineer"
    assert repository.jobs == [job]


def test_get_job_strips_job_id(
    service: JobService,
) -> None:
    job = service.add_job(
        company="OpenAI",
        position="AI Engineer",
    )

    result = service.get_job(
        f"  {job.id}\n"
    )

    assert result is job


def test_update_job_changes_fields_and_preserves_identity(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    existing_job = service.add_job(
        company="OpenAI",
        position="Python Engineer",
        url="https://example.com/jobs/1",
    )

    updated_job = service.update_job(
        job_id=existing_job.id,
        company="OpenAI China",
        position="AI Engineer",
        url="https://example.com/jobs/2",
        note="Interview preparation",
        status=JobStatus.INTERVIEW,
    )

    assert updated_job.id == existing_job.id
    assert updated_job.created_at == existing_job.created_at
    assert updated_job.company == "OpenAI China"
    assert updated_job.position == "AI Engineer"
    assert updated_job.status is JobStatus.INTERVIEW
    assert repository.get_by_id(
        existing_job.id
    ) is updated_job


def test_delete_job_removes_job(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    job = service.add_job(
        company="OpenAI",
        position="AI Engineer",
    )

    deleted_job = service.delete_job(job.id)

    assert deleted_job is job
    assert repository.jobs == []


def test_filter_by_status_returns_matching_jobs(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    pending_job = Job(
        company="OpenAI",
        position="AI Engineer",
        status=JobStatus.PENDING,
    )
    interview_job = Job(
        company="Anthropic",
        position="Research Engineer",
        status=JobStatus.INTERVIEW,
    )
    repository.save(pending_job)
    repository.save(interview_job)

    result = service.filter_by_status(
        JobStatus.INTERVIEW
    )

    assert result == [interview_job]


@pytest.mark.parametrize(
    ("keyword", "expected_positions"),
    [
        (
            "  OPENAI  ",
            ["AI Engineer"],
        ),
        (
            "engineer",
            [
                "AI Engineer",
                "Research Engineer",
            ],
        ),
    ],
)
def test_search_jobs_matches_company_or_position(
    keyword: str,
    expected_positions: list[str],
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    repository.save(
        Job(
            company="OpenAI",
            position="AI Engineer",
        )
    )
    repository.save(
        Job(
            company="Anthropic",
            position="Research Engineer",
        )
    )
    repository.save(
        Job(
            company="ByteDance",
            position="Data Scientist",
        )
    )

    result = service.search_jobs(keyword)

    assert [
        job.position
        for job in result
    ] == expected_positions


def test_search_jobs_rejects_empty_keyword(
    service: JobService,
) -> None:
    with pytest.raises(
        ValidationError,
        match="搜索关键词不能为空",
    ):
        service.search_jobs("   ")


def test_add_job_rejects_exact_duplicate(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    service.add_job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
    )

    with pytest.raises(
        ValidationError,
        match="该岗位可能重复",
    ):
        service.add_job(
            company="OpenAI",
            position="AI Engineer",
            url="https://example.com/jobs/1",
        )

    assert len(repository.jobs) == 1


def test_add_job_allows_different_url(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    first_job = service.add_job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
    )

    second_job = service.add_job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/2",
    )

    assert repository.jobs == [
        first_job,
        second_job,
    ]


def test_update_job_rejects_duplicate_of_another_job(
    service: JobService,
    repository: FakeJobRepository,
) -> None:
    first_job = service.add_job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
    )
    second_job = service.add_job(
        company="Anthropic",
        position="Research Engineer",
        url="https://example.com/jobs/2",
    )

    with pytest.raises(
        ValidationError,
        match="该岗位可能重复",
    ):
        service.update_job(
            job_id=second_job.id,
            company=first_job.company,
            position=first_job.position,
            url=first_job.url,
            note="",
            status=JobStatus.PENDING,
        )

    stored_second_job = repository.get_by_id(
        second_job.id
    )

    assert stored_second_job is second_job
    assert stored_second_job.company == "Anthropic"