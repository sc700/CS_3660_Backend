from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import hashlib
from repositories.user_repository import add_user

router = APIRouter(prefix="/api", tags=["Authentication"])

class SignUpRequest(BaseModel):
    name: str
    username:str
    email: str
    password: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_request: SignUpRequest):
    new_user = add_user(signup_request.dict())
    if not new_user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"message": "User created successfully", "user": new_user}
