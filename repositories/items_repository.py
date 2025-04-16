from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.items_model import Item


class ItemsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_items(self, username: str):
        result = await self.db.execute(select(Item).where(Item.username == username))
        return result.scalars().all()

    async def add_user_item(self, username: str, item_data: dict):
        item = Item(username=username, **item_data)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_user_item(self, username: str, item_id: int, updated_data: dict):
        result = await self.db.execute(select(Item).where(Item.id == item_id, Item.username == username))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        for key, value in updated_data.items():
            if value is not None:
                setattr(item, key, value)

        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete_user_item(self, username: str, item_id: int) -> bool:
        result = await self.db.execute(select(Item).where(Item.id == item_id, Item.username == username))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        await self.db.delete(item)
        await self.db.commit()
        return True