from neomodel import db

from models.user import User
from .labels import User as DbUser



class UserRepository:
    def create(self, user: User):
        dbuser = DbUser.nodes.get_or_none(uid=user.id)
        if dbuser is not None:
            raise Exception
        self._encode(user).save()

    def update(self, user: User):
        dbuser = DbUser.nodes.get_or_none(uid=user.id)
        if dbuser is None:
            raise Exception
        self._encde(user).save()

    def delete(self, userId: str):
        user = DbUser.nodes.get_or_none(uid=userId)
        user.delete()
        return self._decode(user)

    def findById(self, userId: str):
        user = DbUser.nodes.get_or_none(uid=userId)
        return self._decode(user)

    def findAll(self):
        return [self._decode(user) for user in DbUser.nodes.all()]

    def _encode(self, user: User):
        return DbUser(
            uid=user.id,
            name=user.name
        )

    def _decode(self, user: DbUser):
        return User(**user.__properties__) if user is not None else None

