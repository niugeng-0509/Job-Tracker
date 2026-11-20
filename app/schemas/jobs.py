"""岗位请求和响应 Schema。"""

from datetime import date, datetime
from uuid import UUID

from pydantic import Field, field_validator

from app.domain import JobStatus
from app.schemas.base import ApiModel
from app.schemas.validators import validate_http_url


class JobCreate(ApiModel):
    company: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=20000)
    url: str = Field(default="", max_length=2048)
    note: str = Field(default="", max_length=5000)
    priority: int = Field(default=0, ge=0, le=5)
    deadline: date | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return validate_http_url(value)


class JobUpdate(ApiModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    position: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=20000)
    url: str | None = Field(default=None, max_length=2048)
    note: str | None = Field(default=None, max_length=5000)
    status: JobStatus | None = None
    priority: int | None = Field(default=None, ge=0, le=5)
    deadline: date | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str | None) -> str | None:
        return None if value is None else validate_http_url(value)


class JobResponse(ApiModel):
    id: UUID
    company: str
    position: str
    description: str
    url: str
    note: str
    status: JobStatus
    priority: int
    deadline: date | None
    created_at: datetime
    updated_at: datetime


class JobPage(ApiModel):
    items: list[JobResponse]
    total: int
    page: int
    page_size: int
