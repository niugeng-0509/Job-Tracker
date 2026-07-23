from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from app.exceptions import ValidationError


class JobStatus(str, Enum):
    """岗位当前所处的求职阶段。"""

    PENDING = "待投递"
    APPLIED = "已投递"
    WRITTEN_TEST = "笔试"
    INTERVIEW = "面试"
    OFFER = "Offer"
    REJECTED = "已拒绝"


@dataclass
class Job:
    """一条求职岗位记录。"""

    company: str
    position: str
    url: str = ""
    note: str = ""
    status: JobStatus = JobStatus.PENDING
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """dataclass 创建对象后自动执行字段清理和校验。"""

        self.company = self.company.strip()
        self.position = self.position.strip()
        self.url = self.url.strip()
        self.note = self.note.strip()

        if not self.company:
            raise ValidationError("公司名称不能为空")

        if not self.position:
            raise ValidationError("岗位名称不能为空")

        if self.url and not self.url.startswith(("http://", "https://")):
            raise ValidationError(
                "招聘链接必须以 http:// 或 https:// 开头"
            )

    def mark_updated(self) -> None:
        """刷新岗位记录的更新时间。"""

        self.updated_at = datetime.now(timezone.utc)
        