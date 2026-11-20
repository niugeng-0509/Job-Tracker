"""SQLAlchemy 事务边界与 Repository 组装。"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.exceptions import PersistenceError
from app.repositories import (
    DocumentRepository,
    EventRepository,
    JobRepository,
    TaskRepository,
    UserRepository,
)
from app.repositories.sqlalchemy import (
    SqlAlchemyDocumentRepository,
    SqlAlchemyEventRepository,
    SqlAlchemyJobRepository,
    SqlAlchemyTaskRepository,
    SqlAlchemyUserRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session
        self.users: UserRepository = SqlAlchemyUserRepository(session)
        self.jobs: JobRepository = SqlAlchemyJobRepository(session)
        self.events: EventRepository = SqlAlchemyEventRepository(session)
        self.tasks: TaskRepository = SqlAlchemyTaskRepository(session)
        self.documents: DocumentRepository = SqlAlchemyDocumentRepository(
            session
        )

    def commit(self) -> None:
        try:
            self._session.commit()
        except SQLAlchemyError as error:
            self._session.rollback()
            raise PersistenceError("数据库操作失败") from error

    def rollback(self) -> None:
        self._session.rollback()
