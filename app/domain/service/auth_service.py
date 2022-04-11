from domain.gateway import CredentialGateway
from domain.auth import Credential
from domain.utils import check_type
from injector import inject
from domain.errors import UnauthorizedError


class AuthService:
    @inject
    def __init__(self, gw: CredentialGateway):
        self.__gw = check_type(gw, CredentialGateway)

    def authenticate(self, cred: Credential):
        if not self.exists(cred):
            raise UnauthorizedError("id or password is invalid")

    def withdraw(self, cred: Credential):
        self.authenticate(cred)
        self.__gw.delete(cred)

    def repassword(self, oldCred: Credential, newCred: Credential):
        self.authenticate(oldCred)
        self.__gw.update(newCred)

    def exists(self, cred: Credential):
        found   = self.__gw.findById(cred.userId)
        if found is None:
            return False
        return found.verify(cred.plainPassword())
