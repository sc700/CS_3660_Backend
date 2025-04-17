from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import inject, Provide

from containers import Container
from services.login_service import LoginService
from schemas.user_schema import AccountResponse

router = APIRouter(prefix="/api/account", tags=["AccountDetails"])

@router.get("", response_model=AccountResponse)
@inject
async def get_account_details(
    request: Request,
    login_service: LoginService = Depends(Provide[Container.login_service])
):
    try:
        username = request.state.jwt_payload["sub"]
        user = await login_service.get_user_by_username(username)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))