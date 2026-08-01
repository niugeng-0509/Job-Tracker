import asyncio
from collections.abc import Sequence
from time import perf_counter

from app.exceptions import ValidationError
from app.models import Job


async def fetch_job_description(
    job: Job,
    delay_seconds: float = 0.3,
) -> str:
    """模拟从招聘网站异步获取一个岗位的 JD。"""

    if not job.url:
        raise ValidationError("获取 JD 需要招聘链接")

    if delay_seconds < 0:
        raise ValueError("等待时间不能为负数")

    print(f"开始获取：{job.company} - {job.position}")

    await asyncio.sleep(delay_seconds)

    print(f"完成获取：{job.company} - {job.position}")

    return (
        f"{job.company} 的 {job.position} JD，"
        f"来源：{job.url}"
    )


async def fetch_sequentially(
    jobs: Sequence[Job],
    delay_seconds: float = 0.3,
) -> list[str]:
    """按照顺序逐个获取 JD。"""

    results: list[str] = []

    for job in jobs:
        description = await fetch_job_description(
            job,
            delay_seconds,
        )
        results.append(description)

    return results


async def fetch_concurrently(
    jobs: Sequence[Job],
    delay_seconds: float = 0.3,
) -> list[str]:
    """并发获取多个 JD。"""

    coroutines = [
        fetch_job_description(job, delay_seconds)
        for job in jobs
    ]

    return list(await asyncio.gather(*coroutines))


async def main() -> None:
    jobs = [
        Job(
            company="OpenAI",
            position="AI Engineer",
            url="https://example.com/jobs/1",
        ),
        Job(
            company="Anthropic",
            position="Backend Engineer",
            url="https://example.com/jobs/2",
        ),
        Job(
            company="Google",
            position="Machine Learning Engineer",
            url="https://example.com/jobs/3",
        ),
    ]

    sequential_started = perf_counter()
    sequential_results = await fetch_sequentially(jobs)
    sequential_elapsed = perf_counter() - sequential_started

    print(
        f"\n顺序获取 {len(sequential_results)} 个 JD，"
        f"耗时：{sequential_elapsed:.2f} 秒\n"
    )

    concurrent_started = perf_counter()
    concurrent_results = await fetch_concurrently(jobs)
    concurrent_elapsed = perf_counter() - concurrent_started

    print(
        f"\n并发获取 {len(concurrent_results)} 个 JD，"
        f"耗时：{concurrent_elapsed:.2f} 秒"
    )


if __name__ == "__main__":
    asyncio.run(main())