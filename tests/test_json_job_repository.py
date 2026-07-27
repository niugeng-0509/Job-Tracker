from pathlib import Path

import pytest

from app.exceptions import JobNotFoundError, StorageError
from app.models import Job, JobStatus
from app.repositories import JsonJobRepository


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    """返回每个测试独享的临时 JSON 文件路径。"""

    return tmp_path / "data" / "jobs.json"


@pytest.fixture
def repository(
    data_file: Path,
) -> JsonJobRepository:
    """创建使用临时文件的 JSON Repository。"""

    return JsonJobRepository(data_file)


def test_get_all_returns_empty_when_file_does_not_exist(
    repository: JsonJobRepository,
    data_file: Path,
) -> None:
    jobs = repository.get_all()

    assert jobs == []
    assert not data_file.exists()


def test_save_and_reload_preserves_jobs(
    repository: JsonJobRepository,
    data_file: Path,
) -> None:
    first_job = Job(
        company="OpenAI",
        position="AI Engineer",
        url="https://example.com/jobs/1",
        note="Remote",
        status=JobStatus.INTERVIEW,
    )
    second_job = Job(
        company="Anthropic",
        position="Research Engineer",
        url="https://example.com/jobs/2",
    )

    repository.save(first_job)
    repository.save(second_job)

    restarted_repository = JsonJobRepository(
        data_file
    )
    loaded_jobs = restarted_repository.get_all()

    assert data_file.exists()
    assert loaded_jobs == [
        first_job,
        second_job,
    ]
    assert loaded_jobs[0] is not first_job
    assert list(
        data_file.parent.glob(
            f".{data_file.name}.*.tmp"
        )
    ) == []


def test_get_by_id_returns_saved_job(
    repository: JsonJobRepository,
) -> None:
    job = Job(
        company="OpenAI",
        position="AI Engineer",
    )
    repository.save(job)

    loaded_job = repository.get_by_id(job.id)

    assert loaded_job == job
    assert loaded_job is not job


def test_get_by_id_raises_when_job_does_not_exist(
    repository: JsonJobRepository,
) -> None:
    with pytest.raises(
        JobNotFoundError,
        match="没有找到岗位",
    ):
        repository.get_by_id("missing-id")


def test_update_persists_changed_job(
    repository: JsonJobRepository,
    data_file: Path,
) -> None:
    original_job = Job(
        company="OpenAI",
        position="Python Engineer",
        url="https://example.com/jobs/1",
    )
    repository.save(original_job)

    updated_job = Job(
        id=original_job.id,
        company="OpenAI China",
        position="AI Engineer",
        url="https://example.com/jobs/2",
        note="Interview preparation",
        status=JobStatus.INTERVIEW,
        created_at=original_job.created_at,
    )

    repository.update(updated_job)

    restarted_repository = JsonJobRepository(
        data_file
    )
    loaded_job = restarted_repository.get_by_id(
        original_job.id
    )

    assert loaded_job == updated_job
    assert loaded_job.id == original_job.id
    assert loaded_job.created_at == original_job.created_at
    assert loaded_job.status is JobStatus.INTERVIEW


def test_delete_removes_job_and_preserves_other_jobs(
    repository: JsonJobRepository,
    data_file: Path,
) -> None:
    first_job = Job(
        company="OpenAI",
        position="AI Engineer",
    )
    second_job = Job(
        company="Anthropic",
        position="Research Engineer",
    )
    repository.save(first_job)
    repository.save(second_job)

    deleted_job = repository.delete(
        first_job.id
    )

    restarted_repository = JsonJobRepository(
        data_file
    )
    remaining_jobs = restarted_repository.get_all()

    assert deleted_job == first_job
    assert remaining_jobs == [second_job]


@pytest.mark.parametrize(
    "invalid_content",
    [
        "{broken json",
        '{"jobs": []}',
    ],
)
def test_get_all_converts_invalid_json_to_storage_error(
    invalid_content: str,
    repository: JsonJobRepository,
    data_file: Path,
) -> None:
    data_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    data_file.write_text(
        invalid_content,
        encoding="utf-8",
    )

    with pytest.raises(
        StorageError,
        match="岗位数据读取失败",
    ):
        repository.get_all()

    assert data_file.read_text(
        encoding="utf-8",
    ) == invalid_content