"""岗位相关的业务逻辑。"""

from app.exceptions import ValidationError
from app.models import Job, JobStatus
from app.repositories import JobRepository


class JobService:
    """管理岗位记录的业务服务。"""

    def __init__(self, repository: JobRepository) -> None:
        self._repository = repository

    def add_job(
        self,
        company: str,
        position: str,
        url: str = "",
        note: str = "",
    ) -> Job:
        """创建岗位，并阻止重复岗位。"""

        new_job = Job(
            company=company,
            position=position,
            url=url,
            note=note,
        )

        self._ensure_not_duplicate(new_job)

        return self._repository.save(new_job)

    def list_jobs(self) -> list[Job]:
        """查询全部岗位。"""

        return self._repository.get_all()

    def get_job(self, job_id: str) -> Job:
        """根据岗位 ID 查询岗位。"""

        return self._repository.get_by_id(job_id.strip())

    def update_job(
        self,
        job_id: str,
        company: str,
        position: str,
        url: str,
        note: str,
        status: JobStatus,
    ) -> Job:
        """更新岗位信息。"""

        existing_job = self.get_job(job_id)

        updated_job = Job(
            id=existing_job.id,
            company=company,
            position=position,
            url=url,
            note=note,
            status=status,
            created_at=existing_job.created_at,
        )

        self._ensure_not_duplicate(
            updated_job,
            excluded_job_id=existing_job.id,
        )

        return self._repository.update(updated_job)

    def delete_job(self, job_id: str) -> Job:
        """删除岗位。"""

        return self._repository.delete(job_id.strip())

    def filter_by_status(
        self,
        status: JobStatus,
    ) -> list[Job]:
        """按照岗位状态筛选。"""

        jobs = self._repository.get_all()

        return [
            job
            for job in jobs
            if job.status == status
        ]

    def search_jobs(self, keyword: str) -> list[Job]:
        """搜索公司名称或岗位名称。"""

        cleaned_keyword = keyword.strip()

        if not cleaned_keyword:
            raise ValidationError("搜索关键词不能为空")

        normalized_keyword = cleaned_keyword.casefold()
        jobs = self._repository.get_all()

        return [
            job
            for job in jobs
            if (
                normalized_keyword in job.company.casefold()
                or normalized_keyword in job.position.casefold()
            )
        ]

    def _ensure_not_duplicate(
        self,
        candidate: Job,
        excluded_job_id: str | None = None,
    ) -> None:
        """检查公司、岗位名称和链接是否完全重复。"""

        jobs = self._repository.get_all()

        for job in jobs:
            if job.id == excluded_job_id:
                continue

            is_duplicate = (
                job.company == candidate.company
                and job.position == candidate.position
                and job.url == candidate.url
            )

            if is_duplicate:
                raise ValidationError(
                    "该岗位可能重复："
                    f"{candidate.company} - "
                    f"{candidate.position}"
                )