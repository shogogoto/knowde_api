from models.utils import check_type
from typing import List
import networkx as nx
from .knowde import Knowde, KnowdeLink


class KnowdeGraph:
    def __init__(self, knowdes: List[Knowde]=[]):
        self.__G = nx.DiGraph()
        self.__knowdes = {k.id: k for k in knowdes}
        for k in knowdes:
            self.add(k)

    def add(self, k: Knowde):
        check_type(k, Knowde)
        self.__knowdes[k.id] = k
        self.__G.add_node(k.id, **k.content)
        self.__G.add_edges_from([ln.toTuple() for ln in k.links])
        return k

    def get(self, id: str) -> Knowde:
        return self.__knowdes.get(id)

    @property
    def nodes(self):
        return self.__knowdes.values()

    # @property
    # def nodes(self):
    #     # return dict(self.__G.nodes)
    #     ks = []
    #     for k, v in dict(self.__G.nodes).items():
    #         print(k, v)
    #         ks.append(Knowde(k, **v))
    #     return ks

    @property
    def edges(self):
        return [KnowdeLink(*edge) for edge in self.__G.edges]
