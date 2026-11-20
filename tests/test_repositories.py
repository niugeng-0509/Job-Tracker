from collections.abc import Iterator
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import JobRecord, UserRecord
from app.db.session import Base
from app.domain import JobStatus
from app.repositories.sqlalchemy import SqlAlchemyJobRepository


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    testing_session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    try:
        with testing_session() as session:
            yield session
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_job_repository_filters_by_owner_keyword_and_status(
    db_session: Session,
) -> None:
    first_user = UserRecord(
        id=uuid4(), email="first@example.com", password_hash="hash"
    )
    second_user = UserRecord(
        id=uuid4(), email="second@example.com", password_hash="hash"
    )
    db_session.add_all(
        [
            first_user,
            second_user,
            JobRecord(
                user_id=first_user.id,
                company="OpenAI",
                position="AI Engineer",
                status=JobStatus.INTERVIEW.value,
                priority=5,
            ),
            JobRecord(
                user_id=first_user.id,
                company="Other",
                position="Backend Engineer",
            ),
            JobRecord(
                user_id=second_user.id,
                company="OpenAI",
                position="Private Role",
                status=JobStatus.INTERVIEW.value,
            ),
        ]
    )
    db_session.commit()
    repository = SqlAlchemyJobRepository(db_session)

    items, total = repository.list_owned(
        first_user.id,
        page=1,
        page_size=20,
        status=JobStatus.INTERVIEW,
        keyword="Open",
        sort_by="priority",
        sort_order="desc",
    )

    assert total == 1
    assert [item.company for item in items] == ["OpenAI"]


def test_job_repository_duplicate_can_exclude_current_job(
    db_session: Session,
) -> None:
    user = UserRecord(
        id=uuid4(), email="user@example.com", password_hash="hash"
    )
    job = JobRecord(user_id=user.id, company="OpenAI", position="Engineer")
    db_session.add_all([user, job])
    db_session.commit()
    repository = SqlAlchemyJobRepository(db_session)

    assert repository.has_duplicate(user.id, "OpenAI", "Engineer", "")
    assert not repository.has_duplicate(
        user.id,
        "OpenAI",
        "Engineer",
        "",
        excluded_job_id=job.id,
    )
