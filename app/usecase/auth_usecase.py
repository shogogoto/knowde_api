from injector import inject

from domain.utils import check_type
from domain.gateway import CredentialGateway
from domain.service import AuthService
from domain.auth import Credential, PlainPassword


class AuthUsecase:
    @inject
    def __init__(self, gw: CredentialGateway):
        self.__gw  = check_type(gw, CredentialGateway)
        self.__svc = AuthService(gw)

    def authenticate(self, userId: str, password: str) -> bool:
        cred = self.__toCredential(userId, password)
        self.__svc.authenticate(cred)
        return True

    def signUp(self, userId: str, password: str):
        cred = self.__toCredential(userId, password)
        return self.__gw.create(cred)

    def repassword(self, userId: str, current_password: str, new_password: str):
        currentCred = self.__toCredential(userId, current_password)
        newCred = self.__toCredential(userId, new_password)
        self.__svc.repassword(currentCred, newCred)

    def withdraw(self, userId: str, password: str):
        cred = self.__toCredential(userId, password)
        self.__svc.withdraw(cred)

    def __toCredential(self, userId: str, password: str):
        p    = PlainPassword(password)
        return Credential(userId, p)

