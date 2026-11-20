"""正式后端的数据访问契约。"""

from typing import Literal, Protocol
from uuid import UUID

from app.db.models import (
    ApplicationEventRecord,
    DocumentRecord,
    JobRecord,
    TaskRecord,
    UserRecord,
)
from app.domain import JobStatus

JobSortField = Literal["created_at", "updated_at", "priority", "deadline"]
SortOrder = Literal["asc", "desc"]


class UserRepository(Protocol):
    def get_by_email(self, email: str) -> UserRecord | None: ...
    def get_by_id(self, user_id: UUID) -> UserRecord | None: ...
    def add(self, user: UserRecord) -> None: ...
    def refresh(self, user: UserRecord) -> None: ...


class JobRepository(Protocol):
    def get_owned(self, user_id: UUID, job_id: UUID) -> JobRecord | None: ...
    def has_duplicate(
        self,
        user_id: UUID,
        company: str,
        position: str,
        url: str,
        excluded_job_id: UUID | None = None,
    ) -> bool: ...
    def add(self, job: JobRecord) -> None: ...
    def delete(self, job: JobRecord) -> None: ...
    def refresh(self, job: JobRecord) -> None: ...
    def list_owned(
        self,
        user_id: UUID,
        page: int,
        page_size: int,
        status: JobStatus | None,
        keyword: str | None,
        sort_by: JobSortField,
        sort_order: SortOrder,
    ) -> tuple[list[JobRecord], int]: ...


class EventRepository(Protocol):
    def list_for_job(
        self, user_id: UUID, job_id: UUID
    ) -> list[ApplicationEventRecord]: ...
    def add(self, event: ApplicationEventRecord) -> None: ...
    def refresh(self, event: ApplicationEventRecord) -> None: ...


class TaskRepository(Protocol):
    def list_owned(
        self, user_id: UUID, completed: bool | None
    ) -> list[TaskRecord]: ...
    def get_owned(self, user_id: UUID, task_id: UUID) -> TaskRecord | None: ...
    def add(self, task: TaskRecord) -> None: ...
    def refresh(self, task: TaskRecord) -> None: ...


class DocumentRepository(Protocol):
    def list_owned(self, user_id: UUID) -> list[DocumentRecord]: ...
    def get_owned(
        self, user_id: UUID, document_id: UUID
    ) -> DocumentRecord | None: ...
    def add(self, document: DocumentRecord) -> None: ...
    def delete(self, document: DocumentRecord) -> None: ...
    def refresh(self, document: DocumentRecord) -> None: ...


class UnitOfWork(Protocol):
    """Service 层依赖的事务和数据访问抽象。"""

    users: UserRepository
    jobs: JobRepository
    events: EventRepository
    tasks: TaskRepository
    documents: DocumentRepository

    def commit(self) -> None: ...
    def rollback(self) -> None: ...
