"""岗位 API 路由。"""

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.api.dependencies import JobServiceDependency
from app.exceptions import (
    ValidationError as JobValidationError,
)
from app.schemas import JobCreate, JobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "岗位重复",
        },
    },
)
def create_job(
    payload: JobCreate,
    service: JobServiceDependency,
) -> JobResponse:
    """创建一个岗位。"""

    try:
        job = service.add_job(
            company=payload.company,
            position=payload.position,
            url=payload.url,
            note=payload.note,
        )
    except JobValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return JobResponse.model_validate(job)
