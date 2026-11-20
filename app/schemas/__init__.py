"""正式 API 请求和响应 Schema。"""

from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse
from app.schemas.documents import DocumentResponse
from app.schemas.events import EventCreate, EventResponse
from app.schemas.jobs import JobCreate, JobPage, JobResponse, JobUpdate
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate

__all__ = [
    "DocumentResponse",
    "EventCreate",
    "EventResponse",
    "JobCreate",
    "JobPage",
    "JobResponse",
    "JobUpdate",
    "RegisterRequest",
    "TaskCreate",
    "TaskResponse",
    "TaskUpdate",
    "TokenResponse",
    "UserResponse",
]
