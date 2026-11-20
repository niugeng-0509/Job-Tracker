from unittest.mock import Mock
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import JobRecord
from app.db.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.exceptions import (
    ConflictError,
    NotFoundError,
    PersistenceError,
)
from app.services import JobService


def test_job_service_rejects_duplicate_before_writing() -> None:
    uow = Mock()
    uow.jobs.has_duplicate.return_value = True
    service = JobService(uow)

    with pytest.raises(ConflictError, match="该岗位可能重复"):
        service.create(uuid4(), "OpenAI", "AI Engineer")

    uow.jobs.add.assert_not_called()
    uow.commit.assert_not_called()


def test_job_service_hides_unowned_or_missing_job() -> None:
    uow = Mock()
    uow.jobs.get_owned.return_value = None
    service = JobService(uow)

    with pytest.raises(NotFoundError, match="岗位不存在"):
        service.get(uuid4(), uuid4())


def test_job_service_commits_and_refreshes_created_job() -> None:
    uow = Mock()
    uow.jobs.has_duplicate.return_value = False
    service = JobService(uow)

    result = service.create(uuid4(), "OpenAI", "AI Engineer", priority=5)

    assert isinstance(result, JobRecord)
    assert result.priority == 5
    uow.jobs.add.assert_called_once_with(result)
    uow.commit.assert_called_once_with()
    uow.jobs.refresh.assert_called_once_with(result)


def test_unit_of_work_rolls_back_failed_commit() -> None:
    session = Mock(spec=Session)
    session.commit.side_effect = SQLAlchemyError("boom")
    uow = SqlAlchemyUnitOfWork(session)

    with pytest.raises(PersistenceError, match="数据库操作失败"):
        uow.commit()

    session.rollback.assert_called_once_with()
