"""文件元数据响应 Schema。"""

from datetime import datetime
from uuid import UUID

from app.schemas.base import ApiModel


class DocumentResponse(ApiModel):
    id: UUID
    job_id: UUID | None
    document_type: str
    filename: str
    content_type: str
    size_bytes: int
    parse_status: str
    created_at: datetime
