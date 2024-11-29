import uuid
from dataclasses import dataclass
from uuid import UUID

#
# @dataclass(frozen=True)
# class UserName:
#     first_name: str
#     surname: str


class User:

    def __init__(
            self,
            user_id: UUID | None = None,
            nickname: str | None = None,
            email: str | None = None,

            first_name: str | None = None,
            surname: str | None = None,
    ):
        if not user_id:
            self.user_id = uuid.uuid4

        if not nickname and not email:
            raise ValueError('No nickname and email provided')

        self.user_id = user_id

        if nickname is not None:
            self.nickname = nickname

        if email is not None:
            self.email = email

        if first_name is not None:
            self.first_name = first_name

        if surname is not None:
            self.surname = surname

    @property
    def full_name(self):
        return "{f_name} {surname}".format(f_name=self.first_name, surname=self.surname)


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "nickname": self.nickname,
            "email": self.email,
            "first_name": self.first_name,
            "surname": self.surname
        }
