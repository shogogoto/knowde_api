from domain.gateway import CredentialGateway
from domain.auth import Credential
from domain.user import User
from domain.utils import check_type
from injector import inject

class AuthService:
    @inject
    def __init__(self, gw: CredentialGateway):
        self.__gw = check_type(gw, CredentialGateway)

    def authenticate(self, cred: Credential):
        user: User = self.__gw.findByCredential(cred)
        cred.verify(user.hashed_password)
        if user is None:
            authorize_excepotion("Could not validate credentials")
        return user

    def repassword(self, oldCred: Credential, newCred: Credential):
        self.authenticate(oldCred)
        self.__db.update(oldCred, newCred)

    def deleteCredential(self, cred: Credential):
        if not self.exists(cred):
            raise ValueError("id or password is invalid")
        self.__gw.delete(cred)

    def repassword(self, oldCred: Credential, newCred: Credential):
        if not self.exists(oldCred):
            raise ValueError("id or password is invalid")
        check_type(newCred, Credential)
        self.__gw.update(newCred)

    def exists(self, cred: Credential):
        check_type(cred, Credential)
        found   = self.__gw.findById(cred.userId)
        if found is None:
            return False
        return found.verify(cred.plainPassword())
