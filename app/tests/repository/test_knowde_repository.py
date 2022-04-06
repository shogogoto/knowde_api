import pytest

from repository import KnowdeRepository

# from domain.space import Space, SpaceRoot
from domain.core import Knowde
from domain.core import KnowdeGraph

from repository.errors import AlreadyExistsError, NotFoundError

# MATCH (n) DETACH DELETE n

# userId = "space_owner"
repo = KnowdeRepository()


@pytest.fixture(scope="module")
def fn():
    pass
    # cred = Credential(userId, PlainPassword("password"))
    # if cRepo.findById(userId) is None:
    #     cRepo.create(cred)
    # yield
    # if cRepo.findById(userId) is not None:
    #     cRepo.delete(cred)

# def test_create(fn):
#     k = Knowde(name="k1", id="k1")
#     k = repo.create(k)
#     found = repo.findById("k1")
#     assert k == found
#     repo.delete(k.id)
#     # k2 = Knowde("k2", id="k2")
#     # repo.createDestination(k.id, k2)
#     # k3 = Knowde("k3", id="k3")
#     # repo.createSource(k.id, k3)
#
def test_batch_create_and_delete(fn):
    k1 = Knowde(name="k1", id="k1")
    k2 = Knowde(name="k2", id="k2", sources=[k1])
    k3 = Knowde(name="k3", id="k3", sources=[k1])
    k4 = Knowde(name="k4", id="k4", sources=[k1])
    k5 = Knowde(name="k5", id="k5", sources=[k1])
    g = KnowdeGraph([k1, k2, k3, k4, k5])
    repo.createBatch(g)
    # repo.deleteBatch(g)
