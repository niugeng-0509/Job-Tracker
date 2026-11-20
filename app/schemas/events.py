"""岗位时间线 Schema。"""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import ApiModel


class EventCreate(ApiModel):
    event_type: str = Field(min_length=1, max_length=100)
    note: str = Field(default="", max_length=5000)
    occurred_at: datetime | None = None


class EventResponse(ApiModel):
    id: UUID
    job_id: UUID
    event_type: str
    note: str
    occurred_at: datetime
