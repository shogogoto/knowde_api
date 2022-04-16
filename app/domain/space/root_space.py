from .base_space import BaseSpace
from domain.utils import check_type
from anytree.node.anynode import AnyNode


# Userと同義
class SpaceRoot(BaseSpace):
    def __init__(self, userId: str, children=None):
        self.__dict__["id"] = check_type(userId, str)
        self.name = "root"
        super().__init__(parent=None, children=children)

    @AnyNode.parent.setter
    def parent(self, value):
        if value is not None:
            raise ValueError("SpaceRoot cant't have parent")


