from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    description: str

class ItemListResponse(BaseModel):
    items: List[Item]