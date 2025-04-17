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
    email: str
    role: Optional[str] = "User"

class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str
    username: str

class AccountResponse(BaseModel):
    username: str
    name: str
    email: str

    class Config:
        from_attributes = True 