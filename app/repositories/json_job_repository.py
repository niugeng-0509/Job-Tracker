"""使用 JSON 文件保存岗位数据。"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from app.exceptions import (
    JobNotFoundError,
    StorageError,
    ValidationError,
)
from app.models import Job, JobStatus


class JsonJobRepository:
    """使用 JSON 文件实现岗位数据的增删改查。"""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)

    def get_all(self) -> list[Job]:
        """查询全部岗位。"""

        return self._read_all()

    def get_by_id(self, job_id: str) -> Job:
        """根据岗位 ID 查询岗位。"""

        jobs = self._read_all()

        for job in jobs:
            if job.id == job_id:
                return job

        raise JobNotFoundError(f"没有找到岗位：{job_id}")

    def save(self, job: Job) -> Job:
        """保存一个新岗位。"""

        jobs = self._read_all()
        jobs.append(job)
        self._write_all(jobs)

        return job

    def update(self, job: Job) -> Job:
        """更新一个已经存在的岗位。"""

        jobs = self._read_all()

        for index, existing_job in enumerate(jobs):
            if existing_job.id == job.id:
                jobs[index] = job
                self._write_all(jobs)
                return job

        raise JobNotFoundError(f"没有找到岗位：{job.id}")

    def delete(self, job_id: str) -> Job:
        """删除岗位，并返回被删除的岗位。"""

        jobs = self._read_all()

        for index, job in enumerate(jobs):
            if job.id == job_id:
                deleted_job = jobs.pop(index)
                self._write_all(jobs)
                return deleted_job

        raise JobNotFoundError(f"没有找到岗位：{job_id}")

    def _read_all(self) -> list[Job]:
        """读取 JSON 文件并恢复为 Job 对象列表。"""

        if not self._file_path.exists():
            return []

        try:
            with self._file_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                raw_data = json.load(file)

            if not isinstance(raw_data, list):
                raise ValueError("JSON 文件最外层必须是列表")

            return [
                self._dict_to_job(item)
                for item in raw_data
            ]

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
            AttributeError,
            ValidationError,
        ) as error:
            raise StorageError(
                f"岗位数据读取失败：{error}"
            ) from error

    def _write_all(self, jobs: list[Job]) -> None:
        """先写入临时文件，再安全替换正式文件。"""

        temporary_path: Path | None = None

        try:
            self._file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = [
                self._job_to_dict(job)
                for job in jobs
            ]

            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._file_path.parent,
                prefix=f".{self._file_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)

                json.dump(
                    data,
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                )

                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            os.replace(
                temporary_path,
                self._file_path,
            )

        except (OSError, TypeError, ValueError) as error:
            raise StorageError(
                f"岗位数据保存失败：{error}"
            ) from error

        finally:
            if (
                temporary_path is not None
                and temporary_path.exists()
            ):
                try:
                    temporary_path.unlink()
                except OSError:
                    pass

    @staticmethod
    def _job_to_dict(job: Job) -> dict[str, Any]:
        """将 Job 对象转换成可写入 JSON 的字典。"""

        return {
            "id": job.id,
            "company": job.company,
            "position": job.position,
            "url": job.url,
            "note": job.note,
            "status": job.status.value,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
        }

    @staticmethod
    def _dict_to_job(data: Any) -> Job:
        """将 JSON 字典恢复为 Job 对象。"""

        if not isinstance(data, dict):
            raise ValueError("每条岗位数据必须是 JSON 对象")

        return Job(
            id=data["id"],
            company=data["company"],
            position=data["position"],
            url=data.get("url", ""),
            note=data.get("note", ""),
            status=JobStatus(data["status"]),
            created_at=datetime.fromisoformat(
                data["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                data["updated_at"]
            ),
        )