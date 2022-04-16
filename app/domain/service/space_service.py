from domain.gateway import SpaceGateway
from domain.space import Space
from domain.utils import check_type
from injector import inject
from domain.errors import SpaceNameDuplicateError


class SpaceService:
    @inject
    def __init__(self, gw: SpaceGateway):
        self.__gw = check_type(gw, SpaceGateway)

    def create(self, space):
        pass
    # def deleteSpace(self, cred: Credential):
    #     self.authenticate(cred)
    #     self.__gw.delete(cred)

    def exists(self, space: Space):
        found = self.__gw.findById(space.id)
        return found is not None

    def isDuplicateName(self, spaceId: str, name: str):
        space = self.__gw.findBatch(spaceId)
        names = [c.name for c in space.children]
        return name in names

    def isRoot(self, s: Space):
        pass
