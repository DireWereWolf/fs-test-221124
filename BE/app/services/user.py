from app.db.database import DatabaseService

from app.db.models.user import User


class UserService():
    def __init__(self):
        self.db = DatabaseService()

    def get_user(
            self,
            _id,
    ):
        user = self.db.get(User, _id)

        return user