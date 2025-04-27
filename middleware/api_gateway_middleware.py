from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings

app = FastAPI()

class ApiGatewayAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        api_token_header = request.headers.get("x-api-token")
        if not api_token_header or api_token_header != settings.api_gateway_token:
            return JSONResponse(status_code=403, content={"detail": "invalid api token"})
        
        response = await call_next(request)
        return response