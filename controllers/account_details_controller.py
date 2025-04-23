from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from containers import Container
from services.login_service import LoginService
from schemas.user_schema import AccountResponse, UpdateAccountSchema

router = APIRouter(prefix="/api/account", tags=["AccountDetails"])

@router.get("", response_model=AccountResponse)
@inject
def get_account_details(
    request: Request,
    login_service: LoginService = Depends(Provide[Container.login_service])
):
    try:
        username = request.state.jwt_payload["sub"]
        user = login_service.user_repository.get_user_by_username(username)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{username}", response_model=AccountResponse)
@inject
def update_account_details(
    username: str,
    updated_fields: UpdateAccountSchema,
    login_service: LoginService = Depends(Provide[Container.login_service])
):
    try:
        user = login_service.user_repository.update_user_account(username, updated_fields.dict())
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))