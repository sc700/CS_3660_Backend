from fastapi import APIRouter, HTTPException
from schemas.login_schema import LoginRequest, LoginResponse, VerifyLoginRequest
from services.login_service import LoginService


router = APIRouter(prefix="/api/login", tags=["Authentication"])

@router.post("/", response_model=LoginResponse)
async def login(login: LoginRequest):
    try:
        token = LoginService.get_login_token(login.username, login.password)
        return LoginResponse(success=True, jwt_token=token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.post("/verify", response_model=LoginResponse)
async def verify(verify_request: VerifyLoginRequest):
    try:
        _ = LoginService.verify_token(verify_request.jwt_token)
        return LoginResponse(success=True, jwt_token=verify_request.jwt_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))