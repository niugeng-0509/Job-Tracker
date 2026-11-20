"""Bearer Token 解析与当前用户依赖。"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.dependencies.database import SettingsDependency
from app.api.dependencies.services import AuthServiceDependency
from app.core.security import decode_access_token
from app.db.models import UserRecord
from app.domain.exceptions import InvalidCredentialsError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: SettingsDependency,
    service: AuthServiceDependency,
) -> UserRecord:
    try:
        user_id = decode_access_token(token, settings)
    except ValueError as error:
        raise InvalidCredentialsError("无法验证身份") from error
    return service.get_user(user_id)


CurrentUser = Annotated[UserRecord, Depends(get_current_user)]
