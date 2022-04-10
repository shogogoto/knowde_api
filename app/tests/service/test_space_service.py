import pytest
from dependency import DIContainer
from repository import SpaceRepository
from domain.service import AuthService
from domain.auth import Space, PlainPassword
from repository.errors import AlreadyExistsError, NotFoundError
from domain.errors import UnauthorizedError


repo = SpaceRepository()

# MATCH (n) DETACH DELETE n

userId = "test_id"
pwd = "password"
# cred = Space(userId, PlainPassword(pwd))

service = DIContainer().resolve(AuthService)


@pytest.fixture(scope="function")
def fn():
    if repo.findById(userId) is not None:
        repo.delete(cred)
    yield
    if repo.findById(userId) is not None:
        repo.delete(cred)

@pytest.mark.slow
def test_fail_repassword(fn):
    pass
