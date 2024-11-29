import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4, UUID
from src.provision.domain import models
from src.provision.service_layer.services import UserNotFound
from src.provision.service_layer.unit_of_work import AbstractUnitOfWork
from src.provision.adapters.repository import AbstractRepository, PaginatedResult
from src.provision.service_layer import services


class FakeRepository(AbstractRepository):
    def __init__(self, users: list[models.User]):
        # sort here needed to prevent of jumping order caused by uuid
        self._users = set(sorted(users, key=lambda user: user.nickname))

    def add(self, user):
        self._users.add(user)

    def get(self, user_id):
        return next((u for u in self._users if u.user_id == user_id), None)

    def delete(self, user_id) -> None:
        return next((u for u in self._users if u.user_id != user_id), None)

    def get_many(self, page: int = None, limit: int = None):
        users_list = list(self._users)

        if page is not None and limit is not None:
            offset = (page - 1) * limit
            paginated_items = users_list[offset:offset + limit]

            return PaginatedResult(
                items=list(paginated_items),
                total=len(self._users)
            )

        return list(self._users)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.mark.asyncio
async def test_create_user():
    repo_mock = FakeRepository([])
    uow_mock = FakeUnitOfWork()
    # Force share of repo for in memory storage (real case has session and doesnt need this)
    uow_mock.users = repo_mock

    # Act
    created_user = services.create_user(
        uow=uow_mock,
        repo=repo_mock,
        nickname="test_nickname",
        email="test@example.com",
        first_name="John",
        surname="Doe",
    )

    # Assert
    assert created_user is not None
    assert isinstance(created_user.user_id, UUID)
    assert created_user.nickname == "test_nickname"
    assert created_user.email == "test@example.com"
    assert created_user.first_name == "John"
    assert created_user.surname == "Doe"

    # Instead of checking calls we verify side effects
    assert uow_mock.committed

class TestGetUsers:

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        # Create the user data
        user_list = [
            models.User(
                user_id=uuid4(),
                nickname="user1",
                email="user1@example.com",
                first_name="First1",
                surname="Last1",
            ),
            models.User(
                user_id=uuid4(),
                nickname="user2",
                email="user2@example.com",
                first_name="First2",
                surname="Last2",
            ),
        ]
        # Sort the user list
        user_list_sorted = sorted(user_list, key=lambda u: u.nickname)

        # Mock repository with sorted users
        self.repo_mock = FakeRepository(user_list_sorted)

    @pytest.mark.asyncio
    async def test_get_users(self):
        result = services.get_users(repo=self.repo_mock)

        # Assert
        assert result is not None
        assert len(result) == 2
        assert isinstance(result[0], models.User)

        assert result[0].nickname == "user1"
        assert result[1].email == "user2@example.com"

    @pytest.mark.asyncio
    async def test_get_users__paginated(self):
        paginated_result = services.get_users(repo=self.repo_mock, page=1, limit=1)
        assert isinstance(paginated_result, PaginatedResult)
        assert len(paginated_result.items) == 1
        assert paginated_result.total == 2

class TestUpdateUser:
    @pytest.mark.asyncio
    async def test_update_user(self):
        user_id = uuid4()

        repo_mock = FakeRepository([models.User(
            user_id=user_id,
            nickname="test_nickname"
        )])
        uow_mock = FakeUnitOfWork()
        # Force share of repo for in memory storage (real case has session and doesnt need this)
        uow_mock.users = repo_mock

        update_data = {
            "nickname": "john_doe",
            "email": "test@test.com",
            "first_name": "John",
            "surname": "Doe"
        }

        result = services.update_user(
            user_id=user_id,
            uow=uow_mock,
            repo=repo_mock,
            **update_data
        )

        assert result is not None
        assert result.nickname == update_data["nickname"]
        assert result.nickname != "test_nickname"
        assert result.email == update_data["email"]
        assert result.first_name == update_data["first_name"]
        assert result.surname == update_data["surname"]

        assert uow_mock.committed

    @pytest.mark.asyncio
    async def test_update_use__not_found(self):
        user_id = uuid4()

        repo_mock = FakeRepository([]) # Empty users
        uow_mock = FakeUnitOfWork()
        # Force share of repo for in memory storage (real case has session and doesnt need this)
        uow_mock.users = repo_mock

        update_data = {
            "nickname": "john_doe",
            "email": "test@test.com",
            "first_name": "John",
            "surname": "Doe"
        }

        with pytest.raises(UserNotFound) as exc_info:
            services.update_user(
                user_id=user_id,
                uow=uow_mock,
                repo=repo_mock,
                **update_data
            )

        assert str(exc_info.value) == f"User with ID {user_id} not found."

@pytest.mark.asyncio
async def test_get_user():
    user_id = uuid4()
    repo_mock = FakeRepository([models.User(
        user_id=user_id,
        nickname="test_nickname"
    )])

    result = services.get_user(
        user_id=user_id,
        repo=repo_mock
    )

    assert result is not None
    assert result.nickname == "test_nickname"

@pytest.mark.asyncio
async def test_delete_user():
    user_id = uuid4()

    repo_mock = FakeRepository([models.User(
        user_id=user_id,
        nickname="test_nickname"
    )])  # Empty users
    uow_mock = FakeUnitOfWork()
    # Force share of repo for in memory storage (real case has session and doesnt need this)
    uow_mock.users = repo_mock

    services.delete_user(
        user_id=user_id,
        uow=uow_mock
    )

