from models.utils import check_type


class User:
    def __init__(self, **kwargs):
        self.__dict__["id"]      = kwargs.get("id")
        self.__dict__["name"]    = kwargs.get("name")
        self.__dict__["created"] = kwargs.get("created")

    def rename(self, name: str):
        self.__dict__["name"] = check_type(name, str)
