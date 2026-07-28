"""Job Tracker 的命令行交互界面。"""

from app.exceptions import JobTrackerError
from app.models import Job, JobStatus
from app.services import JobService


class JobTrackerCLI:
    """负责读取用户输入并显示结果。"""

    def __init__(self, job_service: JobService) -> None:
        self._job_service = job_service

    def run(self) -> None:
        """持续显示菜单，直到用户退出。"""

        while True:
            self._show_menu()
            choice = input("请选择：").strip()

            if choice == "1":
                self._add_job()
            elif choice == "2":
                self._list_jobs()
            elif choice == "3":
                self._update_job()
            elif choice == "4":
                self._delete_job()
            elif choice == "5":
                self._filter_jobs()
            elif choice == "6":
                self._search_jobs()
            elif choice == "7":
                print("程序已退出。")
                return
            else:
                print("选项无效，请重新输入。")

    @staticmethod
    def _show_menu() -> None:
        """显示主菜单。"""

        print("\n===== Job Tracker =====")
        print("1. 添加岗位")
        print("2. 查看全部岗位")
        print("3. 修改岗位")
        print("4. 删除岗位")
        print("5. 按状态筛选")
        print("6. 搜索岗位")
        print("7. 退出")

    def _add_job(self) -> None:
        """读取输入并添加岗位。"""

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
        """显示全部岗位。"""

        try:
            jobs = self._job_service.list_jobs()
        except JobTrackerError as error:
            print(f"岗位读取失败：{error}")
            return

        self._print_job_list(jobs)

    def _update_job(self) -> None:
        """修改岗位信息。"""

        job_id = input("请输入要修改的岗位 ID：").strip()

        try:
            existing_job = self._job_service.get_job(job_id)

            print("直接按回车表示保留原值。")
            print("链接或备注输入 - 表示清空。")

            company_input = input(
                f"公司名称 [{existing_job.company}]："
            ).strip()

            position_input = input(
                f"岗位名称 [{existing_job.position}]："
            ).strip()

            url_input = input(
                f"招聘链接 [{existing_job.url or '未填写'}]："
            ).strip()

            note_input = input(
                f"备注 [{existing_job.note or '未填写'}]："
            ).strip()

            self._show_statuses()

            status_input = input(
                f"岗位状态 [{existing_job.status.value}]："
            ).strip()

            company = company_input or existing_job.company
            position = position_input or existing_job.position

            if url_input == "":
                url = existing_job.url
            elif url_input == "-":
                url = ""
            else:
                url = url_input

            if note_input == "":
                note = existing_job.note
            elif note_input == "-":
                note = ""
            else:
                note = note_input

            status = (
                existing_job.status
                if not status_input
                else JobStatus(status_input)
            )

            updated_job = self._job_service.update_job(
                job_id=job_id,
                company=company,
                position=position,
                url=url,
                note=note,
                status=status,
            )

        except ValueError:
            print("岗位修改失败：无效的岗位状态")
            return
        except JobTrackerError as error:
            print(f"岗位修改失败：{error}")
            return

        print(
            "岗位修改成功："
            f"{updated_job.company} - "
            f"{updated_job.position}"
        )

    def _delete_job(self) -> None:
        """删除岗位，并在删除前确认。"""

        job_id = input("请输入要删除的岗位 ID：").strip()

        try:
            job = self._job_service.get_job(job_id)
        except JobTrackerError as error:
            print(f"岗位查询失败：{error}")
            return

        confirmation = input(
            f'确定删除“{job.company} - {job.position}”吗？(y/n)：'
        ).strip().casefold()

        if confirmation != "y":
            print("已取消删除。")
            return

        try:
            deleted_job = self._job_service.delete_job(job_id)
        except JobTrackerError as error:
            print(f"岗位删除失败：{error}")
            return

        print(
            "岗位删除成功："
            f"{deleted_job.company} - "
            f"{deleted_job.position}"
        )

    def _filter_jobs(self) -> None:
        """按照状态筛选岗位。"""

        self._show_statuses()
        status_input = input("请输入岗位状态：").strip()

        try:
            status = JobStatus(status_input)
            jobs = self._job_service.filter_by_status(status)
        except ValueError:
            print("筛选失败：无效的岗位状态")
            return
        except JobTrackerError as error:
            print(f"筛选失败：{error}")
            return

        self._print_job_list(jobs)

    def _search_jobs(self) -> None:
        """按照公司名称或岗位名称搜索。"""

        keyword = input("请输入搜索关键词：")

        try:
            jobs = self._job_service.search_jobs(keyword)
        except JobTrackerError as error:
            print(f"搜索失败：{error}")
            return

        if not jobs:
            print("没有找到符合条件的岗位。")
            return

        self._print_job_list(jobs)

    @staticmethod
    def _show_statuses() -> None:
        """显示所有允许使用的岗位状态。"""

        print("可选状态：")

        for status in JobStatus:
            print(f"- {status.value}")

    def _print_job_list(self, jobs: list[Job]) -> None:
        """显示岗位列表。"""

        if not jobs:
            print("暂时没有符合条件的岗位记录。")
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
        print(f"更新时间：{job.updated_at.isoformat()}")