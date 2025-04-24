from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings

app = FastAPI()

class ApiGatewayAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Check for the API token in the headers
        api_token_header = request.headers.get("x-api-token")
        if not api_token_header or api_token_header != settings.api_gateway_token:
            # Return a 403 response if the token is missing or invalid
            return JSONResponse(status_code=403, content={"detail": "Invalid API token"})

        # If valid, proceed with the request
        response = await call_next(request)
        return response
