from neomodel import db
from neomodel import Relationship
from neo4j.graph import Node

from domain.utils import flatten
from domain import check_type
from domain.space import Space, SpaceRoot, SpaceChain
from .labels import Space as DbSpace, User as DbUser
from .errors import NotFoundError, AlreadyExistsError


class SpaceRepository:
    @db.transaction
    def create(self, userId: str, space: Space):
        dbuser = self.__findUser(userId)
        dbspace = self._encode(space).save()
        dbuser.spaces.connect(dbspace)
        return self._decode(dbspace)

    @db.transaction
    def createSubSpace(self, parentId: str, child:Space):
        check_type(parentId, str)
        p = DbSpace.nodes.get_or_none(uid=parentId)
        if p is None:
            raise NotFoundError()
        c = self._encode(child).save()
        p.subspaces.connect(c)
        return self._decode(c)

    @db.transaction
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

    @db.transaction
    def deleteBatch(self, root:SpaceRoot):
        check_type(root, SpaceRoot)
        def _delete(space):
            DbSpace.nodes.get_or_none(uid=space.id).delete()
            for c in space.children:
                _delete(c)

        for c in root.children:
            _delete(c)

    @db.transaction
    def move(self, targetId: str, parentId: str):
        check_type(targetId, str)
        check_type(parentId, str)
        tgt = DbSpace.nodes.get_or_none(uid=targetId)
        p   = DbSpace.nodes.get_or_none(uid=parentId)
        tgt.parent.replace(p)

    @db.transaction
    def update(self, space: Space):
        check_type(space, Space)
        s = DbSpace.nodes.get_or_none(uid=space.id)
        s.name = s.name
        return self._decode(s.save())

    @db.transaction
    def delete(self, spaceId: str):
        check_type(spaceId, str)
        dbspace = DbSpace.nodes.get_or_none(uid=spaceId)
        if dbspace is None:
            raise NotFoundError
        subs = dbspace.subspaces.all()
        [s.delete() for s in subs]
        dbspace.delete()

    # def findByName(self, name: str):
    #     dbspaces = DbSpace.nodes.
    @db.transaction
    def findByOwner(self, userId: str):
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

    @db.transaction
    def findById(self, spaceId: str):
        check_type(spaceId, str)
        dbs = DbSpace.nodes.get_or_none(uid=spaceId)
        return self._decode(dbs)

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
        return Space(
            name=dbspace.name,
            id=dbspace.uid
        )
