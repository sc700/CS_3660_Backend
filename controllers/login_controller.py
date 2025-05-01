from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import Provide, inject

from containers import Container
from schemas.login_schema import LoginRequest, LoginResponse, VerifyLoginRequest
from services.login_service import LoginService

router = APIRouter(prefix="/api/login", tags=["Authentication"])

@router.post("", response_model=LoginResponse)
@inject
def login(
    login: LoginRequest,
    login_service: LoginService = Depends(Provide[Container.login_service])
):
    try:
        token = login_service.get_login_token(login.username, login.password)
        return LoginResponse(success=True, jwt_token=token)
    
    except Exception as e:
        if hasattr(login_service, "db_session") and login_service.db_session is not None:
            login_service.db_session.rollback()
        raise HTTPException(status_code=401, detail=str(e))
    
    finally:
        if hasattr(login_service, "db_session") and login_service.db_session is not None:
            login_service.db_session.close()



@router.post("/verify", response_model=LoginResponse)
def verify(verify_request: VerifyLoginRequest):
    try:
        _ = LoginService.verify_token(verify_request.jwt_token)
        return LoginResponse(success=True, jwt_token=verify_request.jwt_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
