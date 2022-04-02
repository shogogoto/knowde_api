from neomodel import db

from models.auth import Credential, PlainPassword, HashedPassword
from models import check_type
from .labels import User as DbUser
from .errors import NotFoundError, AlreadyExistsError

class CredentialRepository:
    @db.transaction
    def create(self, cred: Credential):
        check_type(cred, Credential)
        dbuser = DbUser.nodes.get_or_none(uid=cred.userId)
        if dbuser is not None:
            raise AlreadyExistsError()
        self._encode(cred).save()

    @db.transaction
    def update(self, old: Credential, new: Credential):
        check_type(old, Credential)
        check_type(new, Credential)
        dbuser = DbUser.nodes.get_or_none(uid=old.userId)
        if dbuser is None:
            raise NotFoundError()
        if not old.verify(dbuser.hashed_password):
            raise ValueError("old password is invalid")
        DbUser.create_or_update({
                "uid" :old.userId,
                "hashed_password" :new.hash().value
        })

    @db.transaction
    def delete(self, cred: Credential):
        check_type(cred, Credential)
        dbuser = DbUser.nodes.get_or_none(uid=cred.userId)
        if dbuser is None:
            raise ValueError("id or password is invalid")
        if not cred.verify(dbuser.hashed_password):
            raise ValueError("id or password is invalid")
        dbuser.delete()

    @db.transaction
    def findById(self, userId: str) -> Credential:
        check_type(userId, str)
        user = DbUser.nodes.get_or_none(uid=userId)
        return self._decode(user)

    def _encode(self, cred: Credential):
        return DbUser(
            uid=cred.userId,
            hashed_password=cred.hash().value
        )

    def _decode(self, user: DbUser):
        if user is None: return None
        return Credential(
            userId=user.uid,
            password=HashedPassword(user.hashed_password)
        )
