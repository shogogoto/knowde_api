import pytest
from dependency import DIContainer
from repository import CredentialRepository, UserRepository
from domain.service import UserService
from domain.auth import Credential, PlainPassword
from domain.errors import UserNotFoundError
from domain.user import User

repo = CredentialRepository()
R    = UserRepository()

# MATCH (n) DETACH DELETE n

userId = "test_id"
pwd = "password"
cred = Credential(userId, PlainPassword(pwd))

service = DIContainer().resolve(UserService)


@pytest.fixture(scope="function")
def fn():
    if repo.findById(userId) is None:
        repo.create(cred)
    yield
    if repo.findById(userId) is not None:
        repo.delete(cred)

@pytest.mark.slow
def test_fail_rename(fn):
    user = User(id="no_id", name="test_name")
    with pytest.raises(UserNotFoundError) as e:
        service.rename(user)

@pytest.mark.slow
def test_rename(fn):
    name = "test_name"
    assert R.findByName(name) is None
    user = User(id=userId, name=name)
    service.rename(user)
    assert R.findByName(name) is not None
