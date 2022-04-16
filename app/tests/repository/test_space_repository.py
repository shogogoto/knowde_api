import pytest

from repository import CredentialRepository, SpaceRepository

from domain.auth import Credential, PlainPassword
from domain.space import Space
from repository.errors import AlreadyExistsError, NotFoundError

# MATCH (n) DETACH DELETE n

userId = "test_space_repository"

repo = SpaceRepository()
cRepo = CredentialRepository()


@pytest.fixture(scope="module")
def fn():
    pass
    # cred = Credential(userId, PlainPassword("password"))
    # if cRepo.findById(userId) is None:
    #     cRepo.create(cred)
    # yield
    # if cRepo.findById(userId) is not None:
    #     cRepo.delete(cred)

@pytest.mark.slow
def test_create(fn):
    s = Space(name="a")
    t = repo.create(s)
    found = repo.findById(t.id)
    assert found == t
    repo.delete(t.id)

@pytest.mark.slow
def test_create_subspace(fn):
    s1 = Space(name="s1")
    s2 = Space(name="s2")
    s3 = Space(name="s3")
    t1 = repo.create(s1)
    t2 = repo.createSubSpace(t1.id, s2)
    t3 = repo.createSubSpace(t1.id, s3)

    t2.parent = t1
    t3.parent = t1

    found = repo.findBatch(t1.id)
    assert found.json() == t1.json()
    repo.deleteBatch(found)

@pytest.mark.slow
def test_batch_create_and_delete(fn):
    root = Space(id=userId, name="xyz")
    a = Space(name="a", id="a", parent=root)
    Space(name="b",     id="b", parent=a)
    Space(name="c",     id="c", parent=a)
    d = Space(name="d", id="d", parent=root)
    e = Space(name="e", id="e", parent=d)
    Space(name="g",     id="f", parent=e)
    Space(name="f",     id="g", parent=d)
    repo.createBatch(root)
    found   = repo.findBatch(userId)
    assert root == found
    repo.deleteBatch(found)

@pytest.mark.slow
def test_move_subspace(fn):
    root = Space(id=userId, name="vw")
    a = Space(name="a", id="a1", parent=root)
    b = Space(name="b", id="b1", parent=a)
    c = Space(name="c", id="c1", parent=a)
    sub = Space("sub", id="sub1", children= [
        Space(name="d", id="d1"),
        Space(name="e", id="e1"),
        Space(name="f", id="f1")
    ])
    sub.parent = b
    repo.createBatch(root)
    repo.move(sub.id, c.id)
    found = repo.findBatch(userId)
    sub.parent = None
    sub.parent = c
    assert found.json() == root.json()
    repo.deleteBatch(root)


@pytest.mark.slow
def test_update(fn):
    bfr = repo.create(Space(name="before"))
    bfr.name = "after"
    aft = repo.update(bfr)
    found = repo.findById(aft.id)
    assert aft == found
    repo.delete(found.id)


# def test_find_parent(fn):
#     s = repo.create(Space(name="s1"))
