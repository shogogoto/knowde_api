from neomodel import db

from domain.gateway import UserGateway
from domain.user import User
from domain.utils import check_type
from .labels import User as DbUser


class UserRepository(UserGateway):
    def update(self, user: User):
        dbuser = DbUser.nodes.get_or_none(uid=user.id)
        dbuser.name = user.name
        return self._decode(dbuser.save())

    def findById(self, userId: str):
        check_type(userId, str)
        user = DbUser.nodes.get_or_none(uid=userId)
        return self._decode(user)

    def findByName(self, userName: str):
        check_type(userName, str)
        user = DbUser.nodes.get_or_none(name=userName)
        return self._decode(user)

    def findAll(self):
        return [self._decode(user) for user in DbUser.nodes.all()]

    def _encode(self, user: User):
        return DbUser(
            uid=user.id,
            name=user.name,
            created=user.created
        )

    def _decode(self, user: DbUser):
        if user is None:
            return None
        return User(
            id=user.uid,
            name=user.name,
            created=user.created
        )

