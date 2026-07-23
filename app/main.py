"""Job Tracker 程序入口。"""

from app.cli import JobTrackerCLI
from app.services import JobService


def main() -> None:
    """创建项目依赖并启动命令行程序。"""

    job_service = JobService()
    cli = JobTrackerCLI(job_service)
    cli.run()


if __name__ == "__main__":
    main()
    