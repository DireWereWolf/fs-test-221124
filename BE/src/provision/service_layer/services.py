from __future__ import annotations
from uuid import uuid4, UUID

from src.provision.adapters.repository import PaginatedResult
from src.provision.domain import models
from src.provision.service_layer import unit_of_work
from src.provision.adapters import repository


class UserNotFound(Exception):
    pass


def create_user(
        uow: unit_of_work.AbstractUnitOfWork,
        repo: repository.AbstractRepository,

        nickname: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        surname: str | None = None,
) -> models.User:
    user_id = uuid4()

    with uow:
        user_to_create = models.User(
            user_id=user_id,
            nickname=nickname if nickname is not None else None,
            email=email if email is not None else None,
            first_name=first_name if first_name is not None else None,
            surname=surname if surname is not None else None
        )
        uow.users.add(user_to_create)
        uow.commit()

    created_user = repo.get(user_id=user_id)

    return created_user

def get_users(
        repo: repository.AbstractRepository,
        page: int = None,
        limit: int = None
) -> list[models.User] | PaginatedResult:
    result = repo.get_many(
        page=page,
        limit=limit
    )

    return result

def update_user(
        user_id: UUID,
        uow: unit_of_work.AbstractUnitOfWork,
        repo: repository.AbstractRepository,

        nickname: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        surname: str | None = None,
) -> models.User:
    with uow:
        user_to_update = uow.users.get(user_id=user_id)

        if not user_to_update:
            raise UserNotFound(f"User with ID {user_id} not found.")

        if nickname is not None:
            user_to_update.nickname = nickname

        if email is not None:
            user_to_update.email = email

        if first_name is not None:
            user_to_update.first_name = first_name

        if surname is not None:
            user_to_update.surname = surname

        uow.commit()

    updated_user = repo.get(user_id=user_id)

    return updated_user

def get_user(
        user_id: UUID,
        repo: repository.AbstractRepository,
):
    user = repo.get(user_id=user_id)

    return user

def delete_user(
        user_id: UUID,
        uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        uow.users.delete(user_id=user_id)

        uow.commit()
