from injector import inject

from domain.utils import check_type
from domain.gateway import UserGateway
from domain.service import UserService
from domain.user import User


class UserUsecase:
    @inject
    def __init__(self, gw: UserGateway):
        self.__gw  = check_type(gw, UserGateway)
        self.__svc = UserService(gw)

    def rename(self, userId: str, name: str) -> bool:
        user = self.__toUser(userId, name)
        self.__svc.rename(user)

    def __toUser(self, userId: str, name: str):
        return User(id=userId, name=name)

