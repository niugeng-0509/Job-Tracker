"""岗位时间线业务服务。"""

from datetime import datetime, timezone
from uuid import UUID

from app.db.models import ApplicationEventRecord
from app.domain.exceptions import NotFoundError
from app.repositories import UnitOfWork


class EventService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def _require_job(self, user_id: UUID, job_id: UUID) -> None:
        if self._uow.jobs.get_owned(user_id, job_id) is None:
            raise NotFoundError("岗位不存在")

    def list(
        self, user_id: UUID, job_id: UUID
    ) -> list[ApplicationEventRecord]:
        self._require_job(user_id, job_id)
        return self._uow.events.list_for_job(user_id, job_id)

    def create(
        self,
        user_id: UUID,
        job_id: UUID,
        event_type: str,
        note: str,
        occurred_at: datetime | None,
    ) -> ApplicationEventRecord:
        self._require_job(user_id, job_id)
        event = ApplicationEventRecord(
            user_id=user_id,
            job_id=job_id,
            event_type=event_type,
            note=note,
            occurred_at=occurred_at or datetime.now(timezone.utc),
        )
        self._uow.events.add(event)
        self._uow.commit()
        self._uow.events.refresh(event)
        return event
