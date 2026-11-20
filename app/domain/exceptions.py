"""与 HTTP 和数据库实现无关的业务异常。"""


class DomainError(Exception):
    """正式后端业务异常基类。"""


class NotFoundError(DomainError):
    """当前用户看不到指定资源。"""


class ConflictError(DomainError):
    """资源状态或唯一性冲突。"""


class InvalidOperationError(DomainError):
    """请求在业务语义上无效。"""


class InvalidCredentialsError(DomainError):
    """登录凭据或访问令牌无效。"""


class UnsupportedMediaError(DomainError):
    """文件类型或内容不受支持。"""


class PayloadTooLargeError(DomainError):
    """上传内容超过限制。"""


class PersistenceError(DomainError):
    """数据库或文件持久化失败。"""
