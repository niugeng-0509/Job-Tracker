"""岗位资源的 HTTP 适配层。"""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Query, Response, status

from app.api.dependencies.auth import CurrentUser
from app.api.dependencies.services import JobServiceDependency
from app.db.models import JobRecord
from app.domain import JobStatus
from app.schemas import JobCreate, JobPage, JobResponse, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post(
    "", response_model=JobResponse, status_code=status.HTTP_201_CREATED
)
def create_job(
    payload: JobCreate,
    user: CurrentUser,
    service: JobServiceDependency,
) -> JobRecord:
    return service.create(user.id, **payload.model_dump())


@router.get("", response_model=JobPage)
def list_jobs(
    user: CurrentUser,
    service: JobServiceDependency,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: JobStatus | None = Query(None, alias="status"),  # noqa: B008
    keyword: str | None = None,
    sort_by: Literal[
        "created_at", "updated_at", "priority", "deadline"
    ] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> JobPage:
    items, total = service.list(
        user.id,
        page,
        page_size,
        status_filter,
        keyword,
        sort_by,
        sort_order,
    )
    return JobPage(
        items=[JobResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: UUID,
    user: CurrentUser,
    service: JobServiceDependency,
) -> JobRecord:
    return service.get(user.id, job_id)


@router.patch("/{job_id}", response_model=JobResponse)
def patch_job(
    job_id: UUID,
    payload: JobUpdate,
    user: CurrentUser,
    service: JobServiceDependency,
) -> JobRecord:
    return service.update(
        user.id, job_id, payload.model_dump(exclude_unset=True)
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: UUID,
    user: CurrentUser,
    service: JobServiceDependency,
) -> Response:
    service.delete(user.id, job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
