import pytest

from repository import CredentialRepository
from models.auth import Credential, PlainPassword
from repository.errors import AlreadyExistsError, NotFoundError


repo = CredentialRepository()

# MATCH (n) DETACH DELETE n

uid = "test_id"
cred = Credential(uid, PlainPassword("password"))

@pytest.fixture(scope="function")
def fn():
    if repo.findById(uid) is not None:
        repo.delete(cred)
    yield
    # if repo.findById(uid) is not None:
    #     repo.delete(cred)

@pytest.mark.slow
def test_create_cred(fn):
    repo.create(cred)
    assert repo.findById(uid) is not None

@pytest.mark.slow
def test_create_duplicate_id(fn):
    repo.create(cred)
    with pytest.raises(AlreadyExistsError) as e:
        repo.create(cred)

@pytest.mark.slow
def test_not_exists_update(fn):
    with pytest.raises(NotFoundError):
        repo.update(cred, cred)

@pytest.mark.slow
def test_invalid_update(fn):
    repo.create(cred)
    cred2 = Credential(uid, PlainPassword("diff_password"))
    new   = Credential(uid, PlainPassword("new_password"))
    with pytest.raises(ValueError) as e:
        repo.update(cred2, new)

@pytest.mark.slow
def test_update(fn):
    repo.create(cred)
    new_passwd = PlainPassword("new_password")
    new   = Credential(uid, new_passwd)
    repo.update(cred, new)
    found = repo.findById(cred.userId)
    assert found.userId == new.userId
    assert found.verify(new_passwd.value)
    repo.delete(new)




