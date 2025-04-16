from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession
from containers import Container
from services.login_service import LoginService
from schemas.login_schema import LoginRequest, LoginResponse, VerifyLoginRequest
from database.db import get_async_db

router = APIRouter(prefix="/api/login", tags=["Authentication"])

from fastapi import Request

@router.post("", response_model=LoginResponse)
@inject
async def login(
    login: LoginRequest,
    db: AsyncSession = Depends(get_async_db),
    container: Container = Depends(Provide[Container])
):
    try:
        user_repository = container.user_repository_factory(db)
        login_service = LoginService(user_repository_factory=lambda _: user_repository)
        token = await login_service.get_login_token(db, login.username, login.password)
        return LoginResponse(success=True, jwt_token=token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/verify", response_model=LoginResponse)
def verify(verify_request: VerifyLoginRequest):
    try:
        _ = LoginService.verify_token(verify_request.jwt_token)
        return LoginResponse(success=True, jwt_token=verify_request.jwt_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))