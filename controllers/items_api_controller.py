from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.items_repository import get_user_items, add_user_item, delete_user_item, update_user_item

router = APIRouter(prefix="/api/items", tags=["Items"])

class Item(BaseModel):
    id: int = None
    name: str
    details: str = ""
    latitude: float
    longitude: float

class ItemUpdate(BaseModel):
    name: str = None
    description: str = None

@router.get("/users/{username}/items")
async def get_items(username: str):
    items = get_user_items(username)
    return {"items": items}

@router.post("/users/{username}/items")
async def add_item(username: str, item: Item):
    added_item = add_user_item(username, item.dict())
    return {"message": "Item added successfully", "item": added_item}

@router.delete("/users/{username}/items/{item_id}")
async def delete_item(username: str, item_id: int):
    success = delete_user_item(username, item_id)
    if success:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Unable to delete item")
    
@router.put("/users/{username}/items/{item_id}")
async def update_item(username: str, item_id: int, updated_item: ItemUpdate):
    updated = update_user_item(username, item_id, updated_item.dict(exclude_unset=True))
    return {"message": "Item updated successfully", "item": updated}