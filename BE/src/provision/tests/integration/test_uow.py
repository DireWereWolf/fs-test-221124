from uuid import uuid4, UUID

import pytest

from sqlalchemy.sql import text

from src.provision.domain import models
from src.provision.service_layer import unit_of_work

def transform_user_id(user_id: UUID) -> str:
    return str(user_id).replace('-', '')

def get_user(session, user_id):
    result = session.execute(
        text("SELECT user_id FROM users WHERE user_id = :user_id"),
        {"user_id": transform_user_id(user_id)},
    )

    row = result.fetchone()

    return row[0] if row else None

@pytest.mark.asyncio
async def test_uow_can_create_user(session_factory):
    session = session_factory()

    user_id = uuid4()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        user_to_create = models.User(
            user_id=user_id,
            nickname="test_nickname",
        )
        uow.users.add(user_to_create)
        uow.commit()

    created_user_id = get_user(session, user_id=user_id)

    assert created_user_id == transform_user_id(user_id)