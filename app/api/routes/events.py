"""岗位时间线的 HTTP 适配层。"""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.auth import CurrentUser
from app.api.dependencies.services import EventServiceDependency
from app.db.models import ApplicationEventRecord
from app.schemas import EventCreate, EventResponse

router = APIRouter(tags=["events"])


@router.get("/jobs/{job_id}/events", response_model=list[EventResponse])
def list_events(
    job_id: UUID,
    user: CurrentUser,
    service: EventServiceDependency,
) -> list[ApplicationEventRecord]:
    return service.list(user.id, job_id)


@router.post(
    "/jobs/{job_id}/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    job_id: UUID,
    payload: EventCreate,
    user: CurrentUser,
    service: EventServiceDependency,
) -> ApplicationEventRecord:
    return service.create(
        user.id,
        job_id,
        payload.event_type,
        payload.note,
        payload.occurred_at,
    )
