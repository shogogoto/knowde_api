from .base_space import BaseSpace
from typing import List

from anytree.node.exceptions import LoopError
from anytree.util import commonancestors
# find結果が想定と異なる Python 3.4までしか対応してないからか。。
from anytree import cachedsearch as CS
from anytree import search as S
import fastcache

import operator
import functools
from ordered_set import OrderedSet

from domain.utils import check_type


# len(chidren) = 0 or 1
class SpaceChain:
    @classmethod
    def create(cls, spaces: List[BaseSpace]):
        c = None
        for s in spaces:
            s.parent = c
            c = s
        return cls(c)

    @classmethod
    def createByPairs(cls, pair_list: List[List[BaseSpace]]):
        ods    = [OrderedSet(space_pair) for space_pair in pair_list]
        spaces = functools.reduce(operator.or_, ods)
        return cls.create(spaces)

    @classmethod
    def batchMerge(cls, spaceChains):
        if len(spaceChains) == 0:
            return None
        merge = lambda x, y: y.merge(x.root)
        return functools.reduce(merge, spaceChains)

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

    @property
    def root(self):
        return self._space.root

    # @property
    # def leaf(self):
    #     return self._space.leaves[0]

    def __check(self, s:BaseSpace):
        check_type(s, BaseSpace)
        if len(s.root.leaves) >= 2:
            raise ValueError("SpaceChain has only parent and child")

    def merge(self, other: BaseSpace) -> BaseSpace:
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
                chain[i + 1].parent = None
                chain[i + 1].parent = tail

        self.__merged = True
        return other

    def json(self) -> dict:
        self._space.root.json()


class AlreadyMergedError(Exception):
    pass
