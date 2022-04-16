from domain.utils import check_type
from domain.space import Space


class User:
    def __init__(self, id: str, **kwargs):
        self.__id   = check_type(id, str)
        self._dict = kwargs

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self._dict.get("name")

    @property
    def created(self):
        return self._dict.get("created")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created
        }
