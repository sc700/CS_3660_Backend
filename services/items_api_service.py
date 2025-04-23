from schemas.items_schema import ItemListResponse, ItemSchema
from database.db import DatabaseFactory

class ItemsAPIService:
    def __init__(self, items_repository_factory, db_factory: DatabaseFactory):
        self.items_repository_factory = items_repository_factory
        self.db_factory = db_factory

    def get_user_items(self, username: str) -> ItemListResponse:
        with self.db_factory.SessionLocal() as db:
            repo = self.items_repository_factory(db)
            items = repo.get_user_items(username)
            return ItemListResponse(items=[ItemSchema.model_validate(item) for item in items])

    def add_user_item(self, username: str, item_data: dict) -> ItemSchema:
        with self.db_factory.SessionLocal() as db:
            repo = self.items_repository_factory(db)
            return repo.add_user_item(username, item_data)

    def update_user_item(self, username: str, item_id: int, updated_data: dict) -> ItemSchema:
        with self.db_factory.SessionLocal() as db:
            repo = self.items_repository_factory(db)
            return repo.update_user_item(username, item_id, updated_data)

    def delete_user_item(self, username: str, item_id: int) -> bool:
        with self.db_factory.SessionLocal() as db:
            repo = self.items_repository_factory(db)
            return repo.delete_user_item(username, item_id)