import pytest

from repository import CredentialRepository, SpaceRepository

from models.auth import Credential, PlainPassword
from models.space import Space, SpaceRoot
from repository.errors import AlreadyExistsError, NotFoundError

# MATCH (n) DETACH DELETE n

userId = "space_owner"

repo = SpaceRepository()
cRepo = CredentialRepository()


@pytest.fixture(scope="module")
def fn():
    cred = Credential(userId, PlainPassword("password"))
    if cRepo.findById(userId) is None:
        cRepo.create(cred)
    yield
    # if cRepo.findById(userId) is not None:
    #     cRepo.delete(cred)

# 子が一括で削除される
# childrenを一括Move
def test_create(fn):
    s = Space(name="a")
    t = repo.create(userId, s)
    found = repo.findById(t.id)
    assert found == t
    repo.delete(t.id)

def test_create_subspace(fn):
    s1 = Space(name="s1")
    s2 = Space(name="s2")
    s3 = Space(name="s3")
    t1 = repo.create(userId, s1)
    t2 = repo.createSubSpace(t1.id, s2)
    t3 = repo.createSubSpace(t1.id, s3)

    root = SpaceRoot(userId)
    t1.parent = root
    t2.parent = t1
    t3.parent = t1

    found = repo.findByOwner(userId)
    assert found == root
    for c in found.children:
        repo.delete(c.id)

def test_batch_create_and_delete(fn):
    root = SpaceRoot(userId)
    a = Space(name="a", id="a", parent=root)
    Space(name="b",     id="b", parent=a)
    Space(name="c",     id="c", parent=a)
    d = Space(name="d", id="d", parent=root)
    e = Space(name="e", id="e", parent=d)
    Space(name="g",     id="f", parent=e)
    Space(name="f",     id="g", parent=d)

    repo.createBatch(root)
    found   = repo.findByOwner(userId)
    assert root == found
    repo.deleteBatch(found)

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
    repo.move(sub.id, c.id)
    found = repo.findByOwner(userId)

    sub.parent = None
    sub.parent = c
    assert found == root
    repo.deleteBatch(root)

def test_update(fn):
    bfr = repo.create(userId, Space(name="before"))
    bfr.name = "after"
    aft = repo.update(bfr)
    print(bfr)
    print(aft)
    found = repo.findById(aft.id)
    print(found)
    assert aft == found
    repo.delete(found.id)
