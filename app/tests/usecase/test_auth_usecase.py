import pytest

from usecase import AuthUsecase
from dependency import DIContainer
from domain.errors import UnauthorizedError

uc = DIContainer().resolve(AuthUsecase)

@pytest.mark.slow
def test_usecase():
    userId, pwd = "ucusr1", "ucpw1"
    with pytest.raises(UnauthorizedError):
        uc.authenticate(userId, pwd)
    uc.signUp(userId, pwd)
    assert uc.authenticate(userId, pwd)
    newpwd = "ucpw2"
    uc.repassword(userId, pwd, newpwd)
    with pytest.raises(UnauthorizedError):
        uc.withdraw(userId, pwd)
    assert uc.authenticate(userId, newpwd)
    with pytest.raises(UnauthorizedError):
        uc.withdraw(userId, pwd)
    uc.withdraw(userId, newpwd)
    with pytest.raises(UnauthorizedError):
        uc.authenticate(userId, newpwd)
