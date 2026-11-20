"""Repository 契约的 SQLAlchemy 实现。"""

from uuid import UUID

from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.db.models import (
    ApplicationEventRecord,
    DocumentRecord,
    JobRecord,
    TaskRecord,
    UserRecord,
)
from app.domain import JobStatus
from app.repositories.contracts import JobSortField, SortOrder


class SqlAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> UserRecord | None:
        return self._session.scalar(
            select(UserRecord).where(UserRecord.email == email)
        )

    def get_by_id(self, user_id: UUID) -> UserRecord | None:
        return self._session.get(UserRecord, user_id)

    def add(self, user: UserRecord) -> None:
        self._session.add(user)

    def refresh(self, user: UserRecord) -> None:
        self._session.refresh(user)


class SqlAlchemyJobRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_owned(self, user_id: UUID, job_id: UUID) -> JobRecord | None:
        return self._session.scalar(
            select(JobRecord).where(
                JobRecord.id == job_id, JobRecord.user_id == user_id
            )
        )

    def has_duplicate(
        self,
        user_id: UUID,
        company: str,
        position: str,
        url: str,
        excluded_job_id: UUID | None = None,
    ) -> bool:
        statement = select(JobRecord.id).where(
            JobRecord.user_id == user_id,
            JobRecord.company == company,
            JobRecord.position == position,
            JobRecord.url == url,
        )
        if excluded_job_id is not None:
            statement = statement.where(JobRecord.id != excluded_job_id)
        return self._session.scalar(statement) is not None

    def add(self, job: JobRecord) -> None:
        self._session.add(job)

    def delete(self, job: JobRecord) -> None:
        self._session.delete(job)

    def refresh(self, job: JobRecord) -> None:
        self._session.refresh(job)

    def list_owned(
        self,
        user_id: UUID,
        page: int,
        page_size: int,
        status: JobStatus | None,
        keyword: str | None,
        sort_by: JobSortField,
        sort_order: SortOrder,
    ) -> tuple[list[JobRecord], int]:
        filters = [JobRecord.user_id == user_id]
        if status is not None:
            filters.append(JobRecord.status == status.value)
        if keyword:
            pattern = f"%{keyword.strip()}%"
            filters.append(
                or_(
                    JobRecord.company.ilike(pattern),
                    JobRecord.position.ilike(pattern),
                )
            )
        total = (
            self._session.scalar(
                select(func.count()).select_from(JobRecord).where(*filters)
            )
            or 0
        )
        column = getattr(JobRecord, sort_by)
        order = asc(column) if sort_order == "asc" else desc(column)
        statement = (
            select(JobRecord)
            .where(*filters)
            .order_by(order, JobRecord.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(self._session.scalars(statement)), total


class SqlAlchemyEventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_job(
        self, user_id: UUID, job_id: UUID
    ) -> list[ApplicationEventRecord]:
        statement = (
            select(ApplicationEventRecord)
            .where(
                ApplicationEventRecord.user_id == user_id,
                ApplicationEventRecord.job_id == job_id,
            )
            .order_by(ApplicationEventRecord.occurred_at)
        )
        return list(self._session.scalars(statement))

    def add(self, event: ApplicationEventRecord) -> None:
        self._session.add(event)

    def refresh(self, event: ApplicationEventRecord) -> None:
        self._session.refresh(event)


class SqlAlchemyTaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_owned(
        self, user_id: UUID, completed: bool | None
    ) -> list[TaskRecord]:
        statement = select(TaskRecord).where(TaskRecord.user_id == user_id)
        if completed is not None:
            statement = statement.where(TaskRecord.completed == completed)
        return list(
            self._session.scalars(
                statement.order_by(TaskRecord.due_date, TaskRecord.created_at)
            )
        )

    def get_owned(self, user_id: UUID, task_id: UUID) -> TaskRecord | None:
        return self._session.scalar(
            select(TaskRecord).where(
                TaskRecord.id == task_id, TaskRecord.user_id == user_id
            )
        )

    def add(self, task: TaskRecord) -> None:
        self._session.add(task)

    def refresh(self, task: TaskRecord) -> None:
        self._session.refresh(task)


class SqlAlchemyDocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_owned(self, user_id: UUID) -> list[DocumentRecord]:
        return list(
            self._session.scalars(
                select(DocumentRecord)
                .where(DocumentRecord.user_id == user_id)
                .order_by(DocumentRecord.created_at.desc())
            )
        )

    def get_owned(
        self, user_id: UUID, document_id: UUID
    ) -> DocumentRecord | None:
        return self._session.scalar(
            select(DocumentRecord).where(
                DocumentRecord.id == document_id,
                DocumentRecord.user_id == user_id,
            )
        )

    def add(self, document: DocumentRecord) -> None:
        self._session.add(document)

    def delete(self, document: DocumentRecord) -> None:
        self._session.delete(document)

    def refresh(self, document: DocumentRecord) -> None:
        self._session.refresh(document)
