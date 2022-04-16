
class DomainError(Exception):
    status_code: int = 400
    detail: str = "Domain Error"


class UnauthorizedError(DomainError):
    status_code: int = 401
    detail: str = "Unauthorized Error"


class UserNotFoundError(DomainError):
    status_code: int = 404
    detail: str = "User Not Found Error"

class SpaceNameDuplicateError(DomainError):
    status_code: int = 407
    detail: str = "Space name duplicate error"
