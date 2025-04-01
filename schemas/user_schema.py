from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

class User(BaseModel):
    username: str
    name: str
    password_hash: str
    items: List[Item] = []

class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str
    username: str