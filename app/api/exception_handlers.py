"""领域异常到 HTTP 响应的统一转换。"""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    ConflictError,
    DomainError,
    InvalidCredentialsError,
    InvalidOperationError,
    NotFoundError,
    PayloadTooLargeError,
    PersistenceError,
    UnsupportedMediaError,
)


def domain_error_handler(
    _request: Request, exception: Exception
) -> JSONResponse:
    if not isinstance(exception, DomainError):
        raise exception
    error = exception
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: dict[str, str] | None = None

    if isinstance(error, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(error, ConflictError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(error, InvalidOperationError):
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    elif isinstance(error, InvalidCredentialsError):
        status_code = status.HTTP_401_UNAUTHORIZED
        headers = {"WWW-Authenticate": "Bearer"}
    elif isinstance(error, UnsupportedMediaError):
        status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    elif isinstance(error, PayloadTooLargeError):
        status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    elif isinstance(error, PersistenceError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(error)},
        headers=headers,
    )
