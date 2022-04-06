from domain.utils import check_type
from domain.space import Space

class User:
    def __init__(self, **kwargs):
        self.__dict__["id"]      = kwargs.get("id")
        self.__dict__["name"]    = kwargs.get("name")
        self.__dict__["created"] = kwargs.get("created")

    def rename(self, name: str):
        self.__dict__["name"] = check_type(name, str)


    def createSpace(self, **spaceAttrs):
        id = self.__dict__.get("id")
        return Space(id, **spaceAttrs)
        pass
