from injector import inject

from domain.utils import check_type
from domain.gateway import SpaceGateway
from domain.service import SpaceService
from fastapi import HTTPException


class SpaceUsecase:
    @inject
    def __init__(self, gw: SpaceGateway):
        self.__gw  = check_type(gw, SpaceGateway)
        self.__svc = SpaceService(gw)

    def createRoot(self, spaceId: str, name: str):
        s = self._encode(spaceId, name)
        self.__svc.createRoot(s)

    def createSub(self, parentId: str, childId: str, name: str):
        s = self._encode(childId, name)
        self.__gw.createSubSpace(parentId, s)

    def move(self, targetId:str, toId: str):
        self.__svc.move(targetId, toId)

    def delete(self, spaceId: str):
        found = self.__gw.findBatch(spaceId)
        self.__gw.deleteBatch(found)

    def rename(self, spaceId: str, name: str):
        s = self._encode(spaceId, name)
        self.__gw.update(s)

    def _encode(self, spaceId: str, name: str):
        return Space(id=spaceId, name=name)
