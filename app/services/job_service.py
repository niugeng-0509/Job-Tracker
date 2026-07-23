"""岗位相关的业务逻辑。"""

from app.exceptions import JobNotFoundError
from app.models import Job, JobStatus


class JobService:
    """管理岗位记录的业务服务。"""

    def __init__(self) -> None:
        self._jobs: list[Job] = []

    def add_job(
        self,
        company: str,
        position: str,
        url: str = "",
        note: str = "",
    ) -> Job:
        """创建并保存一条岗位记录。"""

        job = Job(
            company=company,
            position=position,
            url=url,
            note=note,
        )

        self._jobs.append(job)
        return job

    def list_jobs(self) -> list[Job]:
        """返回当前全部岗位记录。"""

        return list(self._jobs)

    def get_job(self, job_id: str) -> Job:
        """根据岗位 ID 查询岗位。"""

        for job in self._jobs:
            if job.id == job_id:
                return job

        raise JobNotFoundError(f"没有找到岗位：{job_id}")

    def update_status(
        self,
        job_id: str,
        new_status: JobStatus,
    ) -> Job:
        """更新指定岗位的状态。"""

        job = self.get_job(job_id)
        job.status = new_status
        job.mark_updated()
        return job