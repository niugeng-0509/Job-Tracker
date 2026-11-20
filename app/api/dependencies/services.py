"""Service 与 Unit of Work 的依赖组装。"""

from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database import SessionDependency, SettingsDependency
from app.db.unit_of_work import SqlAlchemyUnitOfWork
from app.services import (
    AuthService,
    DocumentService,
    EventService,
    JobService,
    TaskService,
)


def get_unit_of_work(session: SessionDependency) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


UnitOfWorkDependency = Annotated[
    SqlAlchemyUnitOfWork, Depends(get_unit_of_work)
]


def get_auth_service(
    uow: UnitOfWorkDependency,
    settings: SettingsDependency,
) -> AuthService:
    return AuthService(uow, settings)


def get_job_service(uow: UnitOfWorkDependency) -> JobService:
    return JobService(uow)


def get_event_service(uow: UnitOfWorkDependency) -> EventService:
    return EventService(uow)


def get_task_service(uow: UnitOfWorkDependency) -> TaskService:
    return TaskService(uow)


def get_document_service(
    uow: UnitOfWorkDependency,
    settings: SettingsDependency,
) -> DocumentService:
    return DocumentService(uow, settings)


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
JobServiceDependency = Annotated[JobService, Depends(get_job_service)]
EventServiceDependency = Annotated[EventService, Depends(get_event_service)]
TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]
DocumentServiceDependency = Annotated[
    DocumentService, Depends(get_document_service)
]
