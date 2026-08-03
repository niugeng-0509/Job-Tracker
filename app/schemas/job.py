"""岗位 API 请求与响应 Schema。"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    TypeAdapter,
    ValidationError,
    field_validator,
    model_validator,
)

from app.models import JobStatus

_HTTP_URL_ADAPTER = TypeAdapter(HttpUrl)


def _validate_http_url(value: str) -> str:
    """允许空字符串，否则要求有效的 HTTP/HTTPS URL。"""

    if not value:
        return value

    try:
        _HTTP_URL_ADAPTER.validate_python(value)
    except ValidationError as error:
        raise ValueError(
            "招聘链接必须是有效的 HTTP 或 HTTPS URL"
        ) from error

    return value


class JobCreate(BaseModel):
    """创建岗位时允许客户端提交的字段。"""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    company: str = Field(
        min_length=1,
        max_length=200,
    )
    position: str = Field(
        min_length=1,
        max_length=200,
    )
    url: str = Field(
        default="",
        max_length=2048,
    )
    note: str = Field(
        default="",
        max_length=5000,
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        """校验非空招聘链接。"""

        return _validate_http_url(value)


class JobUpdate(BaseModel):
    """部分更新岗位时允许客户端提交的字段。"""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    company: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    position: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    url: str | None = Field(
        default=None,
        max_length=2048,
    )
    note: str | None = Field(
        default=None,
        max_length=5000,
    )
    status: JobStatus | None = None

    @field_validator(
        "company",
        "position",
        "url",
        "note",
        "status",
        mode="before",
    )
    @classmethod
    def reject_null(cls, value: object) -> object:
        """字段可以省略，但出现时不能为 null。"""

        if value is None:
            raise ValueError("更新字段不能为 null")

        return value

    @field_validator("url")
    @classmethod
    def validate_url(
        cls,
        value: str,
    ) -> str:
        """校验更新请求中的招聘链接。"""

        return _validate_http_url(value)

    @model_validator(mode="after")
    def reject_empty_update(self) -> JobUpdate:
        """PATCH 请求至少包含一个更新字段。"""

        if not self.model_fields_set:
            raise ValueError("至少提供一个需要更新的字段")

        return self


class JobResponse(BaseModel):
    """返回给 API 客户端的岗位数据。"""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        str_strip_whitespace=True,
    )

    id: UUID
    company: str
    position: str
    url: str
    note: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
