"""AI Job Copilot 正式 FastAPI 应用入口。"""

from fastapi import FastAPI, status

from app.api.exception_handlers import domain_error_handler
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as documents_router
from app.api.routes.events import router as events_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.tasks import router as tasks_router
from app.domain.exceptions import DomainError

app = FastAPI(
    title="AI Job Copilot API",
    version="0.1.0",
)

app.add_exception_handler(DomainError, domain_error_handler)

app.include_router(jobs_router)
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(tasks_router)
app.include_router(documents_router)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["system"],
)
async def health() -> dict[str, str]:
    """返回 API 进程的基本健康状态。"""

    return {"status": "ok"}
