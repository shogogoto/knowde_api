from typing import Union
from models.utils import flatten
from neomodel import db, Q
from neo4j.graph import Node

from models import check_type
from models.core import Knowde
from models.core import KnowdeGraph
from .labels import Knowde as DbKnowde
from .errors import NotFoundError, AlreadyExistsError


class KnowdeRepository:
    @db.transaction
    def create(self, knowde: Knowde):
        dbk = self._encode(knowde).save()
        return self._decode(dbk)

    def createSource(self, destId: str, src: Knowde):
        dest = self.__find(destId)
        dbsrc = self._encode(src).save()
        dest.src.connect(dbsrc)
        return dbsrc

    def createDestination(self, srcId: str, dest: Knowde):
        src = self.__find(srcId)
        dbdest = self._encode(dest).save()
        src.destinations.connect(dbdest)
        return dbdest

    def createBatch(self, g: KnowdeGraph):
        check_type(g, KnowdeGraph)
        print(dir(DbKnowde))
        print(dir(DbKnowde.nodes))
        ks =[self._toJson(n) for n in g.nodes]
        ids =[n.id for n in g.nodes]
        dbks = { dbk.uid: dbk for dbk in DbKnowde.get_or_create(*ks)}
        for edge in g.edges:
            self._connect(edge.srcId, edge.destId, dbks)
        return [self._decode(dbk) for dbk in dbks.values()]

    def delete(self, knowdeId: str):
        dbk = self.__find(knowdeId)
        dbk.delete()

    def deleteBatch(self, g: KnowdeGraph):
        check_type(g, KnowdeGraph)
        ids =[n.id for n in g.nodes]
        params = {"ids": ids}
        result, meta = db.cypher_query("""
            MATCH (k:Knowde)
            WHERE k.uid IN $ids
            DETACH DELETE k
        """, params)
        return result

    def findById(self, knowdeId: str):
        dbk = self.__find(knowdeId)
        return self._decode(dbk)

    def findSources(self, knowdeId: str):
        # dbk = self.__find(knowdeId)
        check_type(knowdeId, str)
        # 関係の深さ*の書き方が非推奨
        params = {"id": knowdeId}
        result, meta = db.cypher_query("""
            MATCH (k1:Knowde)-[r:LINK*]->(k2:Knowde)
            WHERE k2.uid=$id
            RETURN r, k1, k2
        """, params)

        # for row in result:
        #     print(row)
        import networkx as nx
        G = nx.DiGraph()
        result = set(flatten(result))
        rel2edge = lambda rel: tuple(n.get("uid") for n in rel.nodes)
        edges  = [rel2edge(r)  for r in result if not isinstance(r, Node)]

        G = nx.DiGraph()
        G.add_edges_from(edges)

        nodes = {n.get("uid"): {"name": n.get("name")} for n in result if isinstance(n, Node)}
        nx.set_node_attributes(G, values=nodes)
        # edges = []
        # for rel in rels:
        #     s = DbKnowde.inflate(rel.start_node)
        #     e = DbKnowde.inflate(rel.end_node)
        #     # print(s, e)
        #     # G.add_edge(s.id, e.id)
        # print("#############################")
        # print(dict(G.nodes))
        # print(dict(G.edges))
        # print(G.succ)
        # print(G.pred)

    def findDestinations(self):
        pass


    def __find(self, knowdeId: str):
        check_type(knowdeId, str)
        dbk = DbKnowde.nodes.get_or_none(uid=knowdeId)
        if dbk is None:
            raise NotFoundError
        return dbk

    def _encode(self, knowde: Knowde):
        check_type(knowde, Knowde)
        return DbKnowde(
            name=knowde.name,
            uid=knowde.id
        )

    def _decode(self, dbknowde: DbKnowde):
        return Knowde(
            name=dbknowde.name,
            id=dbknowde.uid
        )

    def _toJson(self, knowde: Knowde):
        check_type(knowde, Knowde)
        d = { "uid": knowde.id }
        d.update(knowde.content)
        return d

    def _connect(self, srcId: str, destId: str, savedKnowdes):
        src  = savedKnowdes.get(srcId)
        dest = savedKnowdes.get(destId)
        src.dest.connect(dest)



