from typing import Annotated, List, Union
from uuid import uuid4, UUID

from fastapi import (
    APIRouter,
    Depends,
    Body,
    Query,
    HTTPException
)
from pydantic import parse_obj_as

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.provision import config
from src.provision.entrypoints.schemas.user import UserFull, UserCreate, UsersPaginated, UserUpdate
from src.provision.adapters import orm, repository
from src.provision.adapters.repository import PaginatedResult
from src.provision.service_layer import services, unit_of_work, db
from src.provision.service_layer.services import UserNotFound

orm.start_mappers()

router = APIRouter() # starts on <root>

@router.post(
    "/user",
    response_model=UserFull
)
async def create_user(
    user_creation_data: Annotated[UserCreate, Body],
    session: Annotated[Session, Depends(db.get_session_local)],
):
    new_user = services.create_user(
        uow=unit_of_work.SqlAlchemyUnitOfWork(),
        repo=repository.SqlAlchemyRepository(session),
        **user_creation_data.dict()
    )

    return new_user.to_dict()

@router.patch(
    "/user/{user_id}",
    response_model=UserFull
)
async def patch_user(
    user_id: UUID,
    user_patch_data: Annotated[UserUpdate, Body],
    session: Annotated[Session, Depends(db.get_session_local)],
):
    try:
        updated_user = services.update_user(
            user_id=user_id,
            uow=unit_of_work.SqlAlchemyUnitOfWork(),
            repo=repository.SqlAlchemyRepository(session),
            **user_patch_data.dict()
        )
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user.to_dict()

@router.get(
    "/user/{user_id}",
    response_model=UserFull
)
async def get_user(
    user_id: UUID,
    session: Annotated[Session, Depends(db.get_session_local)]
):
    user = services.get_user(
        user_id=user_id,
        repo=repository.SqlAlchemyRepository(session),
    )

    return user.to_dict()

@router.delete(
    "/user/{user_id}",
    status_code=204
)
async def delete_user(
    user_id: UUID,
):
    services.delete_user(
        user_id=user_id,
        uow=unit_of_work.SqlAlchemyUnitOfWork(),
    )

    return

@router.get(
    "/users",
    response_model=Union[List[UserFull], UsersPaginated],
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "example_pure": {
                            "summary": "Basic example (without request params) - UserFull list",
                            "description": "An example response using UserFull",
                            "value": [UserFull(
                                user_id=uuid4(),
                                nickname="awesome_nickname",
                                email="john@doe.com",
                                first_name="John",
                                surname="Doe"
                            ).model_dump()],
                        },
                        "example_paginated": {
                            "summary": "Paginated example (with req params) - UsersPaginated obj",
                            "description": "An example response using UsersPaginated.",
                            "value": UsersPaginated(
                                items=[UserFull(
                                    user_id=uuid4(),
                                    nickname="awesome_nickname",
                                    email="john@doe.com",
                                    first_name="John",
                                    surname="Doe"
                                ).model_dump()],
                                total=1
                            ).model_dump(),
                        },
                    }
                }
            }
        }
    },
)
async def get_users(
        session: Annotated[Session, Depends(db.get_session_local)],
        page: int | None = Query(default=None),
        limit: int | None = Query(default=None),
):
    res = None
    users = services.get_users(
        page=page,
        limit=limit,
        repo=repository.SqlAlchemyRepository(session)
    )

    if isinstance(users, PaginatedResult):
        res = UsersPaginated(
            items=parse_obj_as(
                List[UserFull],
                [user.to_dict() for user in users.items]
            ),
            total=users.total
        )

    if isinstance(users, list):
        res = [user.to_dict() for user in users]

    if res is None:
        raise HTTPException(status_code=400, detail="None result for users")

    return res
