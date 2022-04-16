from neomodel import (
    db,
    StructuredNode,
    StringProperty,
    IntegerProperty,
    UniqueIdProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
)

from neomodel.cardinality import (
    ZeroOrMore,
    One,
    OneOrMore,
    ZeroOrOne
)
# from neo4j import GraphDatabase, basic_auth

# URI    = "neo4j://localhost:7687" # コンテナ間通信ではlocalhostを使用できない
# URI    = "neo4j://neo4j:7687" # コンテナ間通信ではlocalhostを使用できない
# USR    = "neo4j"
# PASSWD = "knowde"
# auth = basic_auth(USR, PASSWD)


class User(StructuredNode):
    # id              = StringProperty(unique_index=True, required=True)
    uid              = UniqueIdProperty()
    hashed_password = StringProperty()
    name            = StringProperty(index=True)
    created         = DateTimeProperty(default_now=True)
    spaces          = RelationshipTo("Space", "OWN", cardinality=ZeroOrMore)


class Guild(StructuredNode):
    members = RelationshipTo("User", "MEMBER")


class Space(StructuredNode):
    uid        = UniqueIdProperty()
    name       = StringProperty(index=True, required=True)
    owner      = RelationshipFrom("User", "OWN", cardinality=One)
    parent     = RelationshipFrom("Space", "CONTAINS")
    subspaces  = RelationshipTo("Space", "CONTAINS")
    references = RelationshipTo("Reference", "BELONG_TO")
    knowds     = RelationshipTo("Knowde", "BELONG_TO")

    @classmethod
    def findRoots(cls):
        result, meta = db.cypher_query("""
            MATCH (s:Space)
            WHERE NOT ()-->(s)
            AND size((s)-->()) > 1
            RETURN s
        """)
        return [cls.inflate(row[0]) for row in result]

    # relの連鎖取得できなかった
    # def tree(self):
    #     # params =
    #     result, columns = self.cypher("""
    #         MATCH (r)-[rel*]->(s:Space)
    #         WHERE id(r) = $self
    #         RETURN rel, r, s
    #     """)
    #     print(columns)
    #     return [row[0] for row in result]

class Reference(StructuredNode):
    uid    = UniqueIdProperty()
    name   = StringProperty(required=True)
    author = StringProperty()
    url    = StringProperty()


class Knowde(StructuredNode):
    uid  = UniqueIdProperty()
    name = StringProperty(index=True, required=True)
    src  = RelationshipFrom("Knowde", "DEPEND_ON") # sourceという名前が使用済みで使えなかった
    dest = RelationshipTo("Knowde", "DEPEND_ON")


##  個々のユーザのKnowdeを繋ぐ
##    評価が最も高いものを表示する
class GlobalSpace(StructuredNode):
    uid =  UniqueIdProperty()


class GlobalKnowde(StructuredNode):
    uid =  UniqueIdProperty()


class GlobalReference(StructuredNode):
    uid =  UniqueIdProperty()
