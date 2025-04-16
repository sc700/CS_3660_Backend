# schemas/items_schema.py

from pydantic import BaseModel
from typing import List, Optional


class HistoryEntry(BaseModel):
    timestamp: str
    latitude: float
    longitude: float


class ItemSchema(BaseModel):
    id: int
    name: str
    details: str
    latitude: float
    longitude: float
    history: List[HistoryEntry]

    class Config:
        orm_mode = True


class ItemCreateRequest(BaseModel):
    name: str
    details: Optional[str] = None
    latitude: float
    longitude: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    details: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    history: Optional[List[HistoryEntry]] = None


class ItemListResponse(BaseModel):
    items: List[ItemSchema]