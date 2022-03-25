from models.authentication import Credentia, authorize_excepotion
from models.user import User


class AuthenticationService:
    def __init__(self, userDb):
        self._db = userDb

    def authenticate(self, cred: Credential):
        user: User = self._db.findByCredential(cred)

        cred.verify(user.hashed_password)
        if user is None:
            authorize_excepotion("Could not validate credentials")
        return user


