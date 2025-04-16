from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_db
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/api", tags=["Authentication"])

class SignUpRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    signup_request: SignUpRequest,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        repo = UserRepository(db)
        new_user = await repo.add_user(signup_request.dict())
        return {"message": "User created successfully", "user": new_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User creation failed: {e}")