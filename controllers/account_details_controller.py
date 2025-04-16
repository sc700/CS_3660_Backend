from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from containers import Container
from services.login_service import LoginService  # or another service if needed

router = APIRouter(prefix="/api/account", tags=["AccountDetails"])

@router.get("/{username}")
@inject
async def get_account_details(
    username: str,
    login_service: LoginService = Depends(Provide[Container.login_service])
):
    try:
        user = await login_service.get_user_by_username(username)
        return {
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))