from .base_space import BaseSpace

from anytree.node.anynode import AnyNode
from anytree.node.exceptions import LoopError
# find結果が想定と異なる Python 3.4までしか対応してないからか。。
from anytree import cachedsearch as CS
from anytree import search as S
import fastcache

from domain.utils import check_type


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
