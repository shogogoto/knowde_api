from neomodel import db
from neomodel import Relationship
from neo4j.graph import Node

from domain.gateway import SpaceGateway
from domain.utils import flatten
from domain import check_type
from domain.space import Space, SpaceChain
from .labels import Space as DbSpace, User as DbUser
from .errors import NotFoundError, AlreadyExistsError


class SpaceRepository(SpaceGateway):
    def create(self, space: Space):
        dbspace = self._encode(space).save()
        return self._decode(dbspace)

    def createSubSpace(self, parentId: str, child:Space):
        check_type(parentId, str)
        p = DbSpace.nodes.get_or_none(uid=parentId)
        if p is None:
            raise NotFoundError()
        c = self._encode(child).save()
        p.subspaces.connect(c)
        return self._decode(c)

    def createBatch(self, root:Space):
        check_type(root, Space)
        dbs = self._encode(root).save()
        def _create(parent, parentUid):
            p = DbSpace.nodes.get_or_none(uid=parentUid)
            for c in parent.children:
                dbc = self._encode(c).save()
                p.subspaces.connect(dbc)
                _create(c, dbc.uid)

        _create(root, dbs.uid)

    def deleteBatch(self, s:Space):
        check_type(s, Space)
        def _delete(space):
            DbSpace.nodes.get_or_none(uid=space.id).delete()
            for c in space.children:
                _delete(c)
        _delete(s)

    def move(self, targetId: str, toId: str):
        check_type(targetId, str)
        check_type(toId, str)
        tgt = DbSpace.nodes.get_or_none(uid=targetId)
        p   = DbSpace.nodes.get_or_none(uid=toId)
        tgt.parent.replace(p)

    def update(self, space: Space):
        check_type(space, Space)
        s = DbSpace.nodes.get_or_none(uid=space.id)
        s.name = s.name
        return self._decode(s.save())

    def delete(self, spaceId: str):
        check_type(spaceId, str)
        dbspace = DbSpace.nodes.get_or_none(uid=spaceId)
        if dbspace is None:
            raise NotFoundError
        subs = dbspace.subspaces.all()
        [s.delete() for s in subs]
        dbspace.delete()

    def findParent(self, spaceId: str):
        pass

    # def findByName(self, name: str):
    #     dbspaces = DbSpace.nodes.
    def findBatch(self, spaceId: str):
        check_type(spaceId, str)
        # 関係の深さ*の書き方が非推奨
        params = {"id": spaceId}
        result, meta = db.cypher_query("""
            MATCH (r:Space)-[rel:CONTAINS*]->(s:Space)
            WHERE r.uid=$id
            RETURN rel, r, s
        """, params)
        chains = []
        for row in result:
            rels = row[0]
            sps  = [[self._decode(DbSpace.inflate(n)) for n in rel.nodes] for rel in rels]
            chains.append(SpaceChain.createByPairs(sps))
        return SpaceChain.batchMerge(chains)

    def findById(self, spaceId: str):
        check_type(spaceId, str)
        dbs = self.__find(spaceId)
        return self._decode(dbs)

    def findRoots(self):
        result, meta = db.cypher_query("""
            MATCH (s1)-[rel:CONTAINS*]->(s2:Space)
            RETURN rel, s1, s2
        """)
        chains = []
        for row in result:
            rels = row[0]
            sps  = [[self._decode(DbSpace.inflate(n)) for n in rel.nodes] for rel in rels]
            chain = SpaceChain.createByPairs(sps)
            root = Space(id="global_root", name="global_root")
            chain.extendHead(root)
            chains.append(chain)
            chain.root.print()
        return SpaceChain.batchMerge(chains)

    def __find(self, spaceId: str):
        check_type(spaceId, str)
        return DbSpace.nodes.get_or_none(uid=spaceId)

    def _encode(self, space: Space):
        check_type(space, Space)
        return DbSpace(
            name=space.name,
            uid=space.id
        )

    def _decode(self, dbspace: DbSpace):
        if dbspace is None:
            return None
        return Space(
            name=dbspace.name,
            id=dbspace.uid
        )

