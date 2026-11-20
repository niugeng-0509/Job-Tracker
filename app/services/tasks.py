"""待办业务服务。"""

from datetime import date
from uuid import UUID

from app.db.models import TaskRecord
from app.domain.exceptions import InvalidOperationError, NotFoundError
from app.repositories import UnitOfWork


class TaskService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def list(self, user_id: UUID, completed: bool | None) -> list[TaskRecord]:
        return self._uow.tasks.list_owned(user_id, completed)

    def create(
        self,
        user_id: UUID,
        title: str,
        job_id: UUID | None = None,
        due_date: date | None = None,
    ) -> TaskRecord:
        if (
            job_id is not None
            and self._uow.jobs.get_owned(user_id, job_id) is None
        ):
            raise NotFoundError("岗位不存在")
        task = TaskRecord(
            user_id=user_id, title=title, job_id=job_id, due_date=due_date
        )
        self._uow.tasks.add(task)
        self._uow.commit()
        self._uow.tasks.refresh(task)
        return task

    def update(
        self, user_id: UUID, task_id: UUID, updates: dict[str, object]
    ) -> TaskRecord:
        task = self._uow.tasks.get_owned(user_id, task_id)
        if task is None:
            raise NotFoundError("待办不存在")
        if not updates:
            raise InvalidOperationError("至少提供一个更新字段")
        for key, value in updates.items():
            setattr(task, key, value)
        self._uow.commit()
        self._uow.tasks.refresh(task)
        return task
