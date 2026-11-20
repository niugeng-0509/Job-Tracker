"""待办任务的 HTTP 适配层。"""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.auth import CurrentUser
from app.api.dependencies.services import TaskServiceDependency
from app.db.models import TaskRecord
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    user: CurrentUser,
    service: TaskServiceDependency,
    completed: bool | None = None,
) -> list[TaskRecord]:
    return service.list(user.id, completed)


@router.post(
    "", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
def create_task(
    payload: TaskCreate,
    user: CurrentUser,
    service: TaskServiceDependency,
) -> TaskRecord:
    return service.create(user.id, **payload.model_dump())


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: UUID,
    payload: TaskUpdate,
    user: CurrentUser,
    service: TaskServiceDependency,
) -> TaskRecord:
    return service.update(
        user.id, task_id, payload.model_dump(exclude_unset=True)
    )
