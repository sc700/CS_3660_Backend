from sqlalchemy.ext.asyncio import AsyncSession
from dependency_injector import containers, providers
from database.db import AsyncSessionLocal
from repositories.user_repository import UserRepository
from repositories.items_repository import ItemsRepository
from services.login_service import LoginService
from services.items_api_service import ItemsAPIService
from database.db import DatabaseFactory


from dependency_injector import containers, providers
import logging

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "controllers.login_controller",
            "controllers.items_api_controller",
        ]
    )

    logger = providers.Singleton(logging.getLogger, "cs3660-backend")

    db_factory = providers.Singleton(DatabaseFactory)

    user_repository_factory = providers.Factory(
        UserRepository,
        db=db_factory
    )

    items_repository_factory = providers.Factory(
        ItemsRepository,
        db=db_factory
    )

    login_service = providers.Factory(
        LoginService,
        user_repository_factory=user_repository_factory
    )

    items_api_service = providers.Factory(
        ItemsAPIService,
        items_repository=items_repository_factory
    )
