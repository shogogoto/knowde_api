import pytest
from dependency import DIContainer
from repository import CredentialRepository
from domain.service import AuthService
from domain.auth import Credential, PlainPassword
from repository.errors import AlreadyExistsError, NotFoundError
from domain.errors import UnauthorizedError


repo = CredentialRepository()

# MATCH (n) DETACH DELETE n

userId = "test_id"
pwd = "password"
cred = Credential(userId, PlainPassword(pwd))

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
    repo.create(cred)
    cred2 = Credential(userId, PlainPassword("diff_password"))
    new   = Credential(userId, PlainPassword("new_password"))
    with pytest.raises(UnauthorizedError) as e:
        service.repassword(cred2, new)

@pytest.mark.slow
def test_repassword(fn):
    repo.create(cred)
    newpwd = "new_passwd"
    new    = Credential(userId, PlainPassword(newpwd))
    service.repassword(cred, new)
    found = repo.findById(userId)
    assert found.userId == new.userId
    assert found.verify(newpwd)
    repo.delete(new)


@pytest.mark.slow
def test_fail_withdraw(fn):
    repo.create(cred)
    newpwd = "new_passwd"
    new    = Credential(userId, PlainPassword(newpwd))
    with pytest.raises(UnauthorizedError):
        service.withdraw(new)

@pytest.mark.slow
def test_withdraw(fn):
    repo.create(cred)
    service.withdraw(cred)
    assert not service.exists(cred)



