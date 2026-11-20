"""项目的数据仓储。"""

from examples.m1_cli.repositories.job_repository import JobRepository
from examples.m1_cli.repositories.json_job_repository import JsonJobRepository

__all__ = [
    "JobRepository",
    "JsonJobRepository",
]
