from sqlalchemy.ext.asyncio import AsyncSession
from schemas.items_schema import ItemListResponse, ItemSchema

class ItemsAPIService:
    def __init__(self, items_repository):
        self.items_repository = items_repository

    async def get_user_items(self, db: AsyncSession, username: str) -> ItemListResponse:
        items = await self.items_repository.get_user_items(db, username)
        item_list = [ItemSchema.from_orm(item) for item in items]
        return ItemListResponse(items=item_list)

    async def add_user_item(self, db: AsyncSession, username: str, item_data: dict) -> ItemSchema:
        return await self.items_repository.add_user_item(db, username, item_data)

    async def update_user_item(self, db: AsyncSession, username: str, item_id: int, updated_data: dict) -> ItemSchema:
        return await self.items_repository.update_user_item(db, username, item_id, updated_data)

    async def delete_user_item(self, db: AsyncSession, username: str, item_id: int) -> bool:
        return await self.items_repository.delete_user_item(db, username, item_id)