from dependency_injector import containers, providers
from database.db import DatabaseFactory
from repositories.rbac_repository import RbacRepository
from repositories.user_repository import UserRepository
from repositories.items_repository import ItemsRepository
from services.login_service import LoginService
from services.auth_service import AuthorizationService
from services.items_api_service import ItemsAPIService
from services.rbac_service import RbacService
from services.user_service import UserService

import logging

from services.user_service import UserService

# Create a shared logger instance (could be more complex, e.g., module-based)
logger = logging.getLogger("cs3660backend")
logger.setLevel(logging.DEBUG)

# Define a formatter
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create a handler and attach the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "controllers.login_controller",
            "controllers.items_api_controller",
            "controllers.account_details_controller",
            "controllers.location_history_controller",
            "controllers.locations_controller",
            "controllers.signup_api_controller",
            "controllers.rbac_controller",
        ]
    )

    db_factory = providers.Singleton(DatabaseFactory)

    logger = providers.Object(logger)

    user_repository_factory = providers.Factory(UserRepository)

    user_repository = providers.Factory(
        UserRepository,
        db=db_factory
    )

    items_repository = providers.Factory(
        ItemsRepository,
        db=db_factory.provided.get_session.call()
    )

    login_service = providers.Factory(
        LoginService,
        user_repository=user_repository
    )

    items_api_repository = providers.Factory(ItemsRepository)

    items_api_service = providers.Factory(
    ItemsAPIService,
    db_factory=db_factory,
    items_repository_factory=lambda db: ItemsRepository(db)
)


    auth_service = providers.Factory(
    AuthorizationService,
    user_repository=user_repository,
    logger=logger
    )

    rbac_repository = providers.Factory(
        RbacRepository,
        db=db_factory
    )
    rbac_service = providers.Factory(
        RbacService,
        rbac_repository=rbac_repository
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        rbac_repository=rbac_repository,
        logger=logger
    )