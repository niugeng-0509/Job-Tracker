"""认证请求和响应 Schema。"""

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from app.schemas.base import ApiModel


class RegisterRequest(ApiModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(ApiModel):
    id: UUID
    email: EmailStr
    created_at: datetime


class TokenResponse(ApiModel):
    access_token: str
    token_type: str = "bearer"
