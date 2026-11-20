"""待办任务 Schema。"""

from datetime import date, datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import ApiModel


class TaskCreate(ApiModel):
    title: str = Field(min_length=1, max_length=300)
    job_id: UUID | None = None
    due_date: date | None = None


class TaskUpdate(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    due_date: date | None = None
    completed: bool | None = None


class TaskResponse(ApiModel):
    id: UUID
    job_id: UUID | None
    title: str
    due_date: date | None
    completed: bool
    created_at: datetime
