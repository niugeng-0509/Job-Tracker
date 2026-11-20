"""注册和登录的 HTTP 适配层。"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.services import AuthServiceDependency
from app.db.models import UserRecord
from app.schemas import RegisterRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    service: AuthServiceDependency,
) -> UserRecord:
    return service.register(str(payload.email), payload.password)


@router.post("/login", response_model=TokenResponse)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDependency,
) -> TokenResponse:
    return TokenResponse(
        access_token=service.login(form.username, form.password)
    )
