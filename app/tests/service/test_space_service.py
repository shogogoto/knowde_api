import pytest
from dependency import DIContainer
from repository import SpaceRepository
from domain.service import SpaceService
from domain.space import Space
from repository.errors import AlreadyExistsError, NotFoundError
from domain.errors import SpaceNameDuplicateError


repo = SpaceRepository()

# userId = "test_id"
# pwd = "password"

service = DIContainer().resolve(SpaceService)


# @pytest.fixture(scope="function")
# def fn():
#     if repo.findById(userId) is not None:
#         repo.delete(cred)
#     yield
#     if repo.findById(userId) is not None:
#         repo.delete(cred)

@pytest.mark.slow
def test_isDuplicateName():
    s = Space(id="s1", name="s1")
    Space(id="a", name="a", parent=s)
    Space(id="b", name="b", parent=s)
    Space(id="c", name="c", parent=s)

    repo.createBatch(s)
    assert service.isDuplicateName("s1", "a")
    assert not service.isDuplicateName("s1", "xxx")
    repo.deleteBatch(s)


@pytest.mark.slow
def test_createRoot():
    s = Space(id="s1", name="s1")
    assert not service.exists(s)
    service.createRoot(s)
    assert service.exists(s)
    repo.delete(s.id)


@pytest.mark.slow
def test_fail_createRoot():
    s = Space(id="s1", name="s1")
    service.createRoot(s)
    with pytest.raises(SpaceNameDuplicateError):
        service.createRoot(Space(id="s2", name="s1"))
    repo.delete(s.id)


def test_createSub():
    s = Space(id="s1", name="s1")
    service.createRoot(s)
    s2 = Space(id="s2", name="s2")
    service.createSub(s.id, s2)
    repo.delete(s.id)




