"""岗位业务服务。"""

from datetime import date, datetime, timezone
from uuid import UUID

from app.db.models import JobRecord
from app.domain import JobStatus
from app.domain.exceptions import (
    ConflictError,
    InvalidOperationError,
    NotFoundError,
)
from app.repositories import JobSortField, SortOrder, UnitOfWork


class JobService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def _get(self, user_id: UUID, job_id: UUID) -> JobRecord:
        job = self._uow.jobs.get_owned(user_id, job_id)
        if job is None:
            raise NotFoundError("岗位不存在")
        return job

    def create(
        self,
        user_id: UUID,
        company: str,
        position: str,
        description: str = "",
        url: str = "",
        note: str = "",
        priority: int = 0,
        deadline: date | None = None,
    ) -> JobRecord:
        if self._uow.jobs.has_duplicate(user_id, company, position, url):
            raise ConflictError(f"该岗位可能重复：{company} - {position}")
        job = JobRecord(
            user_id=user_id,
            company=company,
            position=position,
            description=description,
            url=url,
            note=note,
            priority=priority,
            deadline=deadline,
        )
        self._uow.jobs.add(job)
        self._uow.commit()
        self._uow.jobs.refresh(job)
        return job

    def list(
        self,
        user_id: UUID,
        page: int,
        page_size: int,
        status: JobStatus | None,
        keyword: str | None,
        sort_by: JobSortField,
        sort_order: SortOrder,
    ) -> tuple[list[JobRecord], int]:
        return self._uow.jobs.list_owned(
            user_id, page, page_size, status, keyword, sort_by, sort_order
        )

    def get(self, user_id: UUID, job_id: UUID) -> JobRecord:
        return self._get(user_id, job_id)

    def update(
        self, user_id: UUID, job_id: UUID, updates: dict[str, object]
    ) -> JobRecord:
        if not updates:
            raise InvalidOperationError("至少提供一个更新字段")
        if any(
            value is None
            for key, value in updates.items()
            if key != "deadline"
        ):
            raise InvalidOperationError("更新字段不能为 null")
        job = self._get(user_id, job_id)
        company = str(updates.get("company", job.company))
        position = str(updates.get("position", job.position))
        url = str(updates.get("url", job.url))
        if self._uow.jobs.has_duplicate(
            user_id, company, position, url, job.id
        ):
            raise ConflictError(f"该岗位可能重复：{company} - {position}")
        for key, value in updates.items():
            setattr(
                job,
                key,
                value.value if isinstance(value, JobStatus) else value,
            )
        job.updated_at = datetime.now(timezone.utc)
        self._uow.commit()
        self._uow.jobs.refresh(job)
        return job

    def delete(self, user_id: UUID, job_id: UUID) -> None:
        self._uow.jobs.delete(self._get(user_id, job_id))
        self._uow.commit()
