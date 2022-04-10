from injector import Injector, singleton as S

from domain import gateway as GW
import repository as Repo


class DIContainer:
    @classmethod
    def config(cls, binder):
        binder.bind(GW.CredentialGateway, Repo.CredentialRepository, scope=S)
        binder.bind(GW.UserGateway, Repo.UserRepository, scope=S)
        binder.bind(GW.SpaceGateway, Repo.SpaceRepository, scope=S)
        binder.bind(GW.KnowdeGateway, Repo.KnowdeRepository, scope=S)

    def __init__(self):
        self.injector = Injector(self.__class__.config)

    def resolve(self, cls):
        return self.injector.get(cls)
