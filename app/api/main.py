"""AI Job Copilot 的 FastAPI 应用入口。"""

from fastapi import FastAPI, status

app = FastAPI(
    title="AI Job Copilot API",
    version="0.1.0",
)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["system"],
)
async def health() -> dict[str, str]:
    """返回 API 进程的基本健康状态。"""

    return {"status": "ok"}