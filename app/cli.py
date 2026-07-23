"""Job Tracker 的命令行交互界面。"""

from app.exceptions import JobTrackerError
from app.models import Job
from app.services import JobService


class JobTrackerCLI:
    """负责读取用户输入并显示结果。"""

    def __init__(self, job_service: JobService) -> None:
        self._job_service = job_service

    def run(self) -> None:
        """持续显示菜单，直到用户选择退出。"""

        while True:
            self._show_menu()
            choice = input("请选择：").strip()

            if choice == "1":
                self._add_job()
            elif choice == "2":
                self._list_jobs()
            elif choice == "0":
                print("程序已退出。")
                return
            else:
                print("选项无效，请重新输入。")

    @staticmethod
    def _show_menu() -> None:
        """显示主菜单。"""

        print("\n===== Job Tracker =====")
        print("1. 添加岗位")
        print("2. 查看岗位")
        print("0. 退出")

    def _add_job(self) -> None:
        """读取输入并调用业务服务添加岗位。"""

        company = input("公司名称：")
        position = input("岗位名称：")
        url = input("招聘链接：")
        note = input("备注：")

        try:
            job = self._job_service.add_job(
                company=company,
                position=position,
                url=url,
                note=note,
            )
        except JobTrackerError as error:
            print(f"岗位添加失败：{error}")
            return

        print(f"岗位添加成功，岗位 ID：{job.id}")

    def _list_jobs(self) -> None:
        """显示当前保存的全部岗位。"""

        jobs = self._job_service.list_jobs()

        if not jobs:
            print("暂时没有岗位记录。")
            return

        print(f"当前共有 {len(jobs)} 条岗位记录。")

        for job in jobs:
            self._print_job(job)

    @staticmethod
    def _print_job(job: Job) -> None:
        """显示一条岗位记录。"""

        print("\n------------------------")
        print(f"岗位 ID：{job.id}")
        print(f"公司：{job.company}")
        print(f"岗位：{job.position}")
        print(f"状态：{job.status.value}")
        print(f"链接：{job.url or '未填写'}")
        print(f"备注：{job.note or '未填写'}")
        print(f"创建时间：{job.created_at.isoformat()}")