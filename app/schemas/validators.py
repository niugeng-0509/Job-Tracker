"""可复用的 Schema 字段校验器。"""

from pydantic import HttpUrl, TypeAdapter, ValidationError

_HTTP_URL_ADAPTER = TypeAdapter(HttpUrl)


def validate_http_url(value: str) -> str:
    if not value:
        return value
    try:
        _HTTP_URL_ADAPTER.validate_python(value)
    except ValidationError as error:
        raise ValueError("招聘链接必须是有效的 HTTP 或 HTTPS URL") from error
    return value
