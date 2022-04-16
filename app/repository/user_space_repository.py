from neomodel import db
from neomodel import Relationship
from neo4j.graph import Node

from domain.utils import flatten
from domain import check_type
from domain.space import Space, SpaceRoot, SpaceChain
from .labels import Space as DbSpace, User as DbUser
from .errors import NotFoundError, AlreadyExistsError


class UserSpaceRepository:
    def create(self, userId: str, space: Space):
        dbuser = self.__findUser(userId)
        dbspace = self._encode(space).save()
        dbuser.spaces.connect(dbspace)
        return self._decode(dbspace)

    def createBatch(self, root:SpaceRoot):
        check_type(root, SpaceRoot)
        dbuser = self.__findUser(root.id)

        def _create(parent, parentUid):
            p = DbSpace.nodes.get_or_none(uid=parentUid)
            for c in parent.children:
                dbc = self._encode(c).save()
                p.subspaces.connect(dbc)
                _create(c, dbc.uid)

        for c in root.children:
            dbc = self._encode(c).save()
            _create(c, dbc.uid)
            dbuser.spaces.connect(dbc)

    def deleteBatch(self, root:SpaceRoot):
        check_type(root, SpaceRoot)
        def _delete(space):
            DbSpace.nodes.get_or_none(uid=space.id).delete()
            for c in space.children:
                _delete(c)

        for c in root.children:
            _delete(c)

    def findBatch(self, userId: str):
        check_type(userId, str)
        # 関係の深さ*の書き方が非推奨
        params = {"id": userId}
        result, meta = db.cypher_query("""
            MATCH (u:User)-[r*]->(s:Space)
            WHERE u.uid=$id
            RETURN r, u, s
        """, params)
        root = SpaceRoot(userId)
        rels = set([r for r in flatten(result) if not isinstance(r, Node)])
        owns = set(rel for rel in rels if rel.type == "OWN")
        contains = rels - owns
        top_spaces = [DbSpace.inflate(own.end_node) for own in owns]
        from anytree import RenderTree
        for fs in top_spaces:
            Space(name=fs.name, id=fs.uid, parent=root)

        chains = []
        for i, contain in enumerate(contains):
            dbspaces = [DbSpace.inflate(n)  for n in contain.nodes]
            spaces   = [self._decode(d) for d in dbspaces]
            chain = SpaceChain.create(spaces)
            chain.merge(root)
        return root

    def __findUser(self, userId: str):
        check_type(userId, str)
        dbuser = DbUser.nodes.get_or_none(uid=userId)
        if dbuser is None:
            raise NotFoundError("space can't make because user is not found")
        return dbuser

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
