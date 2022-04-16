from neomodel import config, install_all_labels
config.DATABASE_URL = "bolt://neo4j:knowde@neo4j:7687"

from .user_repository import UserRepository
from .credential_repository import CredentialRepository
from .user_space_repository import UserSpaceRepository
from .space_repository import SpaceRepository
from .knowde_repository import KnowdeRepository

install_all_labels()
