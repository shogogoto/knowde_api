import pytest

from repository import CredentialRepository
from repository import UserRepository
from domain.auth import Credential, PlainPassword
from domain.user import User

repo = CredentialRepository()
R    = UserRepository()

# MATCH (n) DETACH DELETE n

userId = "test_id"
pwd = "password"
cred = Credential(userId, PlainPassword(pwd))

@pytest.fixture(scope="function")
def fn():
    if repo.findById(userId) is None:
        repo.create(cred)
    yield
    if repo.findById(userId) is not None:
        repo.delete(cred)


@pytest.mark.slow
def test_update(fn):
    newname = "newname"
    u = User(id=userId, name=newname)
    R.update(u)
    found = R.findById(userId)
    assert found.name == newname

@pytest.mark.slow
def test_findByName(fn):
    name = "name"
    found = R.findByName(name)
    assert found is None
    u = User(id=userId, name=name)
    R.update(u)
    found = R.findByName(name)
    assert found.name == name
