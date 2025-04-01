from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from repositories.user_repository import get_user_by_username, update_user_account

router = APIRouter(prefix="/api/account", tags=["Account"])

class AccountDetails(BaseModel):
    username: str
    name: str
    email: str

class AccountUpdate(BaseModel):
    name: str = None
    email: str = None

@router.get("/{username}", response_model=AccountDetails)
async def get_account(username: str):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return AccountDetails(
        username=user.get("username"),
        name=user.get("name"),
        email=user.get("email", "")
    )

@router.put("/{username}", response_model=AccountDetails)
async def update_account(username: str, account_update: AccountUpdate):
    updated_user = update_user_account(username, account_update.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return AccountDetails(
        username=updated_user.get("username"),
        name=updated_user.get("name"),
        email=updated_user.get("email", "")
    )