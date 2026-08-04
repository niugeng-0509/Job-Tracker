"""FastAPI 路由使用的依赖。"""

from pathlib import Path
from typing import Annotated

from fastapi import Depends

from app.repositories import JsonJobRepository
from app.services import JobService


def get_job_service() -> JobService:
    """创建使用本地 JSON 文件的岗位 Service。"""

    project_root = Path(__file__).resolve().parents[2]
    data_file = project_root / "data" / "jobs.json"

    repository = JsonJobRepository(data_file)

    return JobService(repository)


JobServiceDependency = Annotated[
    JobService,
    Depends(get_job_service),
]