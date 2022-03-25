

class RepositoryError(Exception):
    status_code: int = 400
    detail: str      = "Repository error"


class NotFoundError(RepositoryError):
    status_code: int = 404
    detail: str      = "Not found"

class AlreadyExistsError(RepositoryError):
    status_code: int = 409
    detail: str      = "Already exists the resource"
