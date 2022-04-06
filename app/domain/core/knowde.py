from typing import List, Union
from domain.utils import check_type


class Knowde:
    def __init__(self,
            id=None,
            sources = [],
            **kwargs):
        self.__content = kwargs
        self.__id = id
        self.__links = set()

        self.__sources = sources
        for src in sources:
            self.linkFrom(src)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__content.get("name")

    @property
    def content(self):
        return self.__content

    @property
    def links(self):
        return self.__links

    def linkFrom(self, source):
        check_type(source, __class__)
        self.__links.add(KnowdeLink(source.id, self.id))

    @property
    def source(self):
        return self.__sources

    def __str__(self):
        return str(self.__content)

    def __repr__(self):
        return f"{{'id': '{self.__id}', {self.__content}}}"

    def __eq__(self, other):
        check_type(other, __class__)
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class KnowdeLink:
    def __init__(self, srcId: Union[str, int], destId: Union[str, int]):
        check_type(srcId, (str, int))
        if srcId == destId:
            raise ValueError(f"sorceId={srcId} should be different from destId={destId}")
        check_type(destId, str)
        self.__src_dest = (srcId, destId)

    @property
    def srcId(self):
        return self.__src_dest[0]

    @property
    def destId(self):
        return self.__src_dest[1]

    def __hash__(self):
        return hash(self.__src_dest)

    def __eq__(self, other):
        check_type(other, __class__)
        return self.toTuple() == other.toTuple()

    def toTuple(self):
        return self.__src_dest
