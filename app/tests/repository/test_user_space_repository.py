import pytest

from repository import CredentialRepository, UserSpaceRepository, SpaceRepository

from domain.auth import Credential, PlainPassword
from domain.space import Space, SpaceRoot
from repository.errors import AlreadyExistsError, NotFoundError

# MATCH (n) DETACH DELETE n

userId = "space_owner"

repo = UserSpaceRepository()
cRepo = CredentialRepository()
sRepo = SpaceRepository()

@pytest.fixture(scope="module")
def fn():
    cred = Credential(userId, PlainPassword("password"))
    if cRepo.findById(userId) is None:
        cRepo.create(cred)
    yield
    if cRepo.findById(userId) is not None:
        cRepo.delete(cred)

@pytest.mark.slow
def test_create(fn):
    s = Space(name="a")
    t = repo.create(userId, s)
    found = sRepo.findById(t.id)
    assert found == t
    sRepo.delete(t.id)

@pytest.mark.slow
def test_create_subspace(fn):
    s1 = Space(name="s1")
    s2 = Space(name="s2")
    s3 = Space(name="s3")
    t1 = repo.create(userId, s1)
    t2 = sRepo.createSubSpace(t1.id, s2)
    t3 = sRepo.createSubSpace(t1.id, s3)

    root = SpaceRoot(userId)
    t1.parent = root
    t2.parent = t1
    t3.parent = t1

    found = repo.findBatch(userId)
    assert found == root
    for c in found.children:
        sRepo.delete(c.id)

@pytest.mark.slow
def test_batch_create_and_delete(fn):
    root = SpaceRoot(userId)
    a = Space(name="a", id="a", parent=root)
    Space(name="b",     id="b", parent=a)
    Space(name="c",     id="c", parent=a)
    d = Space(name="d", id="d", parent=root)
    e = Space(name="e", id="e", parent=d)
    Space(name="f",     id="f", parent=e)
    Space(name="g",     id="g", parent=d)

    # repo.createBatch(root)
    found   = repo.findBatch(userId)
    assert root == found
    repo.deleteBatch(found)

@pytest.mark.slow
def test_move_subspace(fn):
    root = SpaceRoot(userId)
    a = Space(name="a", id="a", parent=root)
    b = Space(name="b", id="b", parent=a)
    c = Space(name="c", id="c", parent=a)
    sub = Space("sub", id="sub", children= [
        Space(name="d", id="d"),
        Space(name="e", id="e"),
        Space(name="f", id="f")
    ])
    sub.parent = b
    repo.createBatch(root)
    sRepo.move(sub.id, c.id)
    found = repo.findBatch(userId)

    sub.parent = None
    sub.parent = c
    assert found == root
    repo.deleteBatch(root)
