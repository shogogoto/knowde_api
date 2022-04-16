from typing import List
from anytree.node.anynode import AnyNode
from anytree import RenderTree
from domain.utils import check_type


# Spaceとは、Knowdeの依存関係を制限するもの
class BaseSpace(AnyNode):
    @property
    def id(self) -> str:
        return self.__dict__.get("id")

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "children": sorted([c.json() for c in self.children],
                               key=lambda x:x.get("id"))
        }

    def __eq__(self, other):
        check_type(other, __class__)
        if self.id is None:
            return False
        if other.id is None:
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def print(self):
        print(RenderTree(self))
