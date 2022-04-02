from typing import List

from anytree.node.anynode import AnyNode
from anytree.node.exceptions import LoopError
from anytree.util import commonancestors
# find結果が想定と異なる Python 3.4までしか対応してないからか。。
from anytree import cachedsearch as CS
from anytree import search as S
from anytree import RenderTree
import fastcache


from models.utils import check_type


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

class Space(BaseSpace):
    def __init__(self, name: str, parent=None, children=None, **kwargs):
        self.__dict__["name"] = check_type(name, str)
        super().__init__(parent, children, **kwargs)

    @AnyNode.parent.setter
    def parent(self, value):
        check_type(value, BaseSpace)
        if not (value is None or self.id is None):
            founds = S.findall_by_attr(
                node=value.root,
                name="id",
                value=self.id)
            if len(founds) >= 1:
                raise LoopError("Space should have unique id")
        AnyNode.parent.fset(self, value)


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




# len(chidren) = 0 or 1
class SpaceChain:
    @classmethod
    def create(cls, spaces: List[BaseSpace]):
        c = None
        for s in spaces:
            s.parent = c
            c = s
        return cls(c)

    def __init__(self, s: BaseSpace):
        self.__check(s)
        self._space = s
        self.__merged = False

    def extendTail(self, s: BaseSpace):
        self.__check(s)
        s.parent = self._space.leaves[0]
        return s

    def extendHead(self, s: BaseSpace):
        self.__check(s)
        self._space.root.parent = s
        return s

    # @property
    # def root(self):
    #     return self._space.root
    #
    # @property
    # def leaf(self):
    #     return self._space.leaves[0]

    def __check(self, s:BaseSpace):
        check_type(s, BaseSpace)
        if len(s.root.leaves) >= 2:
            raise ValueError("SpaceChain has only parent and child")

    def merge(self, other: BaseSpace) -> Space:
        if self.__merged:
            raise AlreadyMergedError
        check_type(other, BaseSpace)
        leaf   = self._space.leaves[0]
        chain  = leaf.ancestors + (leaf,)
        ids    = [anc.id for anc in leaf.ancestors]
        founds = S.findall(other.root, lambda node: node.id in ids)
        if len(founds) == 0: return
        head   = founds[0]
        tail   = founds[-1]
        if head is not None:
            i = ids.index(head.id)
            if i > 0:
                chain[i - 1].children = [] # childrenを切り離す
                head.parent = chain[i - 1]

        if tail is not None:
            i = ids.index(tail.id)
            if i <= len(ids):
                chain[i + 1].parent = tail

        self.__merged = True

    def json(self) -> dict:
        self._space.root.json()


class AlreadyMergedError(Exception):
    pass

# class SpaceBranchTraversal:
