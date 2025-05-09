from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class HistoryEntry(BaseModel):
    timestamp: datetime
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class ItemSchema(BaseModel):
    id: int
    username: str
    name: str
    details: Optional[str] = None
    longitude: float
    #history: List[HistoryEntry] = []

    class Config:
        from_attributes = True


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