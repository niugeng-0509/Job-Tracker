"""岗位 Repository 接口。"""

from typing import Protocol

from app.models import Job


class JobRepository(Protocol):
    """定义岗位数据访问必须提供的功能。"""

    def get_all(self) -> list[Job]:
        """查询全部岗位。"""
        ...

    def get_by_id(self, job_id: str) -> Job:
        """根据 ID 查询岗位。"""
        ...

    def save(self, job: Job) -> Job:
        """保存一个新岗位。"""
        ...

    def update(self, job: Job) -> Job:
        """更新一个已有岗位。"""
        ...

    def delete(self, job_id: str) -> Job:
        """删除岗位，并返回被删除的岗位。"""
        ...