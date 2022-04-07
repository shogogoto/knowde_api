from neomodel import db

from domain.gateway import CredentialGateway
from domain.auth import Credential, PlainPassword, HashedPassword
from domain import check_type
from .labels import User as DbUser
from .errors import NotFoundError, AlreadyExistsError


class CredentialRepository(CredentialGateway):
    def create(self, cred: Credential):
        check_type(cred, Credential)
        dbuser = DbUser.nodes.get_or_none(uid=cred.userId)
        if dbuser is not None:
            raise AlreadyExistsError()
        return self._encode(cred).save()

    def update(self, cred: Credential):
        check_type(cred, Credential)
        dbuser = DbUser.nodes.get_or_none(uid=cred.userId)
        if dbuser is None:
            raise NotFoundError()
        DbUser.create_or_update({
                "uid" :cred.userId,
                "hashed_password" :cred.hash().value
        })

    def delete(self, cred: Credential):
        check_type(cred, Credential)
        dbuser = DbUser.nodes.get_or_none(uid=cred.userId)
        dbuser.delete()

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
        if user is None:
            return None
        return Credential(
            userId=user.uid,
            password=HashedPassword(user.hashed_password)
        )
