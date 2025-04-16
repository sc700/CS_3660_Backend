from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schema import User, SignUpRequest
from repositories.user_repository import UserRepository
from database.db import get_async_db

router = APIRouter(prefix="/api/account", tags=["Account"])

@router.get("/{username}", response_model=User)
async def get_account(username: str, db: AsyncSession = Depends(get_async_db)):
    repo = UserRepository(db)
    user = await repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(username=user.username, name=user.name, email=user.email)

@router.put("/{username}", response_model=User)
async def update_account(
    username: str,
    account_update: SignUpRequest,
    db: AsyncSession = Depends(get_async_db)
):
    repo = UserRepository(db)
    updated_user = await repo.update_user_account(username, account_update.dict(exclude_unset=True))
    return User(username=updated_user.username, name=updated_user.name, email=updated_user.email)