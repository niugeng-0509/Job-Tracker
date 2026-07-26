"""项目的数据仓储。"""

from app.repositories.job_repository import JobRepository
from app.repositories.json_job_repository import JsonJobRepository

__all__ = [
    "JobRepository",
    "JsonJobRepository",
]