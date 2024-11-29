import abc
from dataclasses import dataclass

from src.provision.domain import models

@dataclass
class PaginatedResult:
    items: list[models.User]
    total: int

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: models.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id) -> models.User:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user_id) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_many(self, *args, **kwargs) -> list[models.User]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user):
        self.session.add(user)

    def get(self, user_id):
        return self.session.query(models.User).filter_by(user_id=user_id).one()

    def delete(self, user_id) -> None:
        user_to_delete = self.get(user_id=user_id)
        self.session.delete(user_to_delete)

    def get_many(
            self, page: int = None, limit: int = None
    ) -> list[models.User] | PaginatedResult:
        """
        Retrieves all users from the database (supports pagination)
        Example calls: .query_users() - general one (doesn't recommended to prod)
                       .query_users(page=1, limit=10) - paginated
                            (retrieves page elements and total amount)
        """
        query = self.session.query(models.User)

        if page is not None and limit is not None:
            offset = (page - 1) * limit
            total = query.count()
            query = query.offset(offset).limit(limit)
            return PaginatedResult(
                items=query.all(),
                total=total
            )

        return query.all()
