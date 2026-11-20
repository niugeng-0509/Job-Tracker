"""认证业务服务。"""

from uuid import UUID

from app.core.config import Settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.models import UserRecord
from app.domain.exceptions import ConflictError, InvalidCredentialsError
from app.repositories import UnitOfWork


class AuthService:
    def __init__(self, uow: UnitOfWork, settings: Settings) -> None:
        self._uow = uow
        self._settings = settings

    def register(self, email: str, password: str) -> UserRecord:
        normalized = email.lower()
        if self._uow.users.get_by_email(normalized) is not None:
            raise ConflictError("邮箱已注册")
        user = UserRecord(
            email=normalized, password_hash=hash_password(password)
        )
        self._uow.users.add(user)
        self._uow.commit()
        self._uow.users.refresh(user)
        return user

    def login(self, email: str, password: str) -> str:
        user = self._uow.users.get_by_email(email.lower())
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("邮箱或密码错误")
        return create_access_token(user.id, self._settings)

    def get_user(self, user_id: UUID) -> UserRecord:
        user = self._uow.users.get_by_id(user_id)
        if user is None:
            raise InvalidCredentialsError("认证信息无效")
        return user
