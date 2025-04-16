from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from database.db import DatabaseFactory
from repositories.user_repository import UserRepository
from services.login_service import LoginService

app = FastAPI()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        PUBLIC_PATHS = {
                        "/", "/health", "/home", "/api/login",
                        "/favicon.ico", "/about", "/signup",
                        "/login","/docs", "/openapi.json", "/redoc"
                        }

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization token"})

        token = auth_header.split("Bearer ")[1]
        try:
            payload = LoginService.verify_token(token)
            request.state.jwt_payload = payload
        except Exception as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})

        return await call_next(request)   