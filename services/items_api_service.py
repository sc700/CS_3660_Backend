from sqlalchemy.ext.asyncio import AsyncSession
from schemas.items_schema import ItemListResponse, ItemSchema
from repositories.items_repository import ItemsRepository
from database.db import DatabaseFactory

class ItemsAPIService:
    def __init__(self, items_repository_factory, db_factory: DatabaseFactory):
        self.items_repository_factory = items_repository_factory
        self.db_factory = db_factory

    async def get_user_items(self, username: str) -> ItemListResponse:
        async with self.db_factory.AsyncSessionLocal() as db:
            repo = self.items_repository_factory(db)
            items = await repo.get_user_items(db, username)
            return ItemListResponse(items=[ItemSchema.from_orm(item) for item in items])

    async def add_user_item(self, username: str, item_data: dict) -> ItemSchema:
        async with self.db_factory.AsyncSessionLocal() as db:
            repo = self.items_repository_factory(db)
            return await repo.add_user_item(db, username, item_data)

    async def update_user_item(self, username: str, item_id: int, updated_data: dict) -> ItemSchema:
        async with self.db_factory.AsyncSessionLocal() as db:
            repo = self.items_repository_factory(db)
            return await repo.update_user_item(db, username, item_id, updated_data)

    async def delete_user_item(self, username: str, item_id: int) -> bool:
        async with self.db_factory.AsyncSessionLocal() as db:
            repo = self.items_repository_factory(db)
            return await repo.delete_user_item(db, username, item_id)