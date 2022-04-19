from domain.gateway import SpaceGateway
from domain.space import Space
from domain.utils import check_type
from injector import inject
from domain.errors import SpaceNameDuplicateError


class SpaceService:
    @inject
    def __init__(self, gw: SpaceGateway):
        self.__gw = check_type(gw, SpaceGateway)

    def createRoot(self, space: Space):
        roots = self.__gw.findRoots()
        if roots is not None:
            names = [root.name for root in roots]
            if space.name in names:
                raise SpaceNameDuplicateError
        self.__gw.create(space)

    def createSub(self, parentId: str, space: Space):
        if self.isDuplicateName(parentId, space.name):
            raise SpaceNameDuplicateError
        self.__gw.createSubSpace(parentId, space)

    def move(self, targetId:str, toId: str):
        s = self.__gw.findById(targetId)
        if self.isDuplicateName(toId, s.name):
            raise SpaceNameDuplicateError
        self.__gw.move(targetId, toId)

    def exists(self, space: Space):
        found = self.__gw.findById(space.id)
        return found is not None

    def isDuplicateName(self, spaceId: str, name: str):
        space = self.__gw.findBatch(spaceId)
        if space is None:
            return False
        names = [c.name for c in space.children]
        return name in names

    def isRoot(self, s: Space):
        pass
