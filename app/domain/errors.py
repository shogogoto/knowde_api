
class DomainError(Exception):
    status_code: int = 400
    detail: str = "Domain Error"


class UnauthorizedError(DomainError):
    status_code: int = 401
    detail: str = "Unauthorized Error"
