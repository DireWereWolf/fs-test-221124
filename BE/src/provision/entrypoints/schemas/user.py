from uuid import UUID

from pydantic import BaseModel

class UserCreate(BaseModel):
    nickname: str | None
    email: str | None
    first_name: str | None
    surname: str | None = None

class UserFull(UserCreate):
    user_id: UUID

class UserUpdate(UserCreate):
    ...

class UsersPaginated(BaseModel):
    items: list[UserFull]
    total: int