from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from services.login_service import LoginService

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, public_paths: list = None):
        super().__init__(app)
        self.public_paths = public_paths or ["/", "/health", "/api/login"]

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.public_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization token"}
            )

        token = auth_header.split("Bearer ")[1]
        try:
            LoginService.verify_token(token)
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e)}
            )

        return await call_next(request)