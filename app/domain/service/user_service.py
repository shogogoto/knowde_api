from domain.gateway import UserGateway
from domain.user import User
from domain.utils import check_type
from injector import inject
from domain.errors import UserNotFoundError

class UserService:
    @inject
    def __init__(self, gw: UserGateway):
        self.__gw = check_type(gw, UserGateway)

    def rename(self, user: User):
        if not self.exists(user):
            raise UserNotFoundError
        return self.__gw.update(user)

    def exists(self, user: User) -> bool:
        found = self.__gw.findById(user.id)
        return found is not None
