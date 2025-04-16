from dependency_injector import containers, providers
import logging

from database.db import get_async_db
from repositories.user_repository import UserRepository
from repositories.items_repository import ItemsRepository
from services.login_service import LoginService
from services.items_api_service import ItemsAPIService

logger = logging.getLogger("cs3660backend")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "controllers.login_controller",
            "controllers.items_api_controller",
            "controllers.locations_controller",
            "controllers.location_history_controller",
            "controllers.account_details_controller",
            "controllers.signup_api_controller",
        ]
    )

    logger = providers.Object(logger)

    user_repository_factory = providers.Factory(
        lambda db: UserRepository(db)
    )

    login_service = providers.Factory(
        LoginService,
        user_repository_factory=user_repository_factory
    )

    items_repository = providers.Factory(ItemsRepository)

    items_api_service = providers.Factory(
        ItemsAPIService,
        items_repository=items_repository
    )