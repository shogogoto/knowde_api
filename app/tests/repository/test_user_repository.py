import pytest

from repository import UserRepository
from models import user as U

repo = UserRepository()

# MATCH (n) DETACH DELETE n

uid = "test_id"
user = U.User(id=uid, name="GTO")

@pytest.fixture
def lifecycle_function():
    yield
    # if repo.findById(uid) is not None:
    #     repo.delete(uid)


# def test_create_cred(lifecycle_function):
#     assert repo.findById(uid) is None
#     repo.create(cred)
#     assert repo.findById(uid) is not None
#
# def test_create_user(lifecycle_function):
#     assert repo.findById(uid) is None
#     user = U.User(id=uid)
#     repo.create(user)
#     assert repo.findById(uid) is not None
#
#
# def test_create_duplicate_id(lifecycle_function):
#     assert repo.findById(uid) is None
#     repo.create(cred)
#     with pytest.raises(Exception) as e:
#         repo.create(cred)
#
