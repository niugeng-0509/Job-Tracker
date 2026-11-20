"""Job Tracker 程序入口。"""

from pathlib import Path

from examples.m1_cli.cli import JobTrackerCLI
from examples.m1_cli.exceptions import JobTrackerError
from examples.m1_cli.repositories import JsonJobRepository
from examples.m1_cli.services import JobService


def main() -> None:
    """创建项目依赖并启动命令行程序。"""

    project_root = Path(__file__).resolve().parents[2]
    data_file = project_root / "data" / "jobs.json"

    try:
        repository = JsonJobRepository(data_file)
        job_service = JobService(repository)
        cli = JobTrackerCLI(job_service)
        cli.run()

    except JobTrackerError as error:
        print(f"程序运行失败：{error}")

    except KeyboardInterrupt:
        print("\n程序已退出。")


if __name__ == "__main__":
    main()
