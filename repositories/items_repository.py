from sqlalchemy import select
from models.items_model import Item
from sqlalchemy.orm import joinedload
from typing import List

class ItemsRepository:
    def __init__(self, db):
        self.db = db

    def get_user_items(self, username: str):
        result = self.db.execute(select(Item).where(Item.username == username))
        return result.scalars().all()
    

    def get_user_items_with_history(self, username: str) -> List[Item]:
        return (
            self.db.query(Item)
            .options(joinedload(Item.history))
            .filter(Item.username == username)
            .all()
        )


    def add_user_item(self, username: str, item_data: dict):
        item = Item(username=username, **item_data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_user_item(self, username: str, item_id: int, updated_data: dict):
        item = self.db.query(Item).filter_by(id=item_id, username=username).first()
        if not item:
            return None
        for key, value in updated_data.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_user_item(self, username: str, item_id: int) -> bool:
        item = self.db.query(Item).filter_by(id=item_id, username=username).first()
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True