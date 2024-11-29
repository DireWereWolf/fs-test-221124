from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserRead
# from app.services.user_service import create_user, get_user

from app.services.user import UserService

router = APIRouter()


@router.post(
    "/",
    # response_model=UserRead
)
def create_user_endpoint(
        # user: UserCreate, db: Session = Depends(get_db)
):
    return
    # return create_user(db, user)


@router.get(
    "/{user_id}",
    # response_model=UserRead
)
def read_user(
        # user_id: int, db: Session = Depends(get_db)
        user_id: UUID,
        user_service: Annotated[UserService, Depends(UserService)]
):
    res = user_service.get_user(_id=user_id)
    # db_user = get_user(db, user_id)
    # if not db_user:
    #     raise HTTPException(status_code=404, detail="User not found")
    # return db_user
    return {}
