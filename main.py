import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from containers import Container
from config import settings
from middleware.api_gateway_middleware import ApiGatewayAuthMiddleware
from middleware.middleware import AuthMiddleware

from controllers import (
    login_controller,
    items_api_controller,
    locations_controller,
    location_history_controller,
    account_details_controller,
    signup_api_controller,
)

from schemas.message_schema import MessageResponse

app = FastAPI(title="CS3660 Backend Project", version="1.0.0")
container = Container()
container.wire(modules=[
    "controllers.login_controller",
    "controllers.items_api_controller",
    "controllers.locations_controller",
    "controllers.location_history_controller",
    "controllers.account_details_controller",
    "controllers.signup_api_controller",
])
app.container = container

app.add_middleware(AuthMiddleware)

if settings.app_env == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if settings.app_env == "prod":
    app.add_middleware(ApiGatewayAuthMiddleware)

app.include_router(login_controller.router)
app.include_router(items_api_controller.router)
app.include_router(locations_controller.router)
app.include_router(location_history_controller.router)
app.include_router(account_details_controller.router)
app.include_router(signup_api_controller.router)

@app.get("/", response_model=MessageResponse)
def root():
    return {"message": "Backend is running!"}

@app.get("/health", response_model=MessageResponse)
def health():
    return {"message": "OK"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="CS3660 Backend Project",
        routes=app.routes,
    )

    
    openapi_schema["openapi"] = "3.0.1"
    
    openapi_schema["paths"] = {
        path.rstrip("/") if path != "/" else path: data 
        for path, data in openapi_schema["paths"].items() if path != ""
    }
   
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        if "properties" in schema:
            for field_name, field in schema["properties"].items():
                if "anyOf" in field:
                    field["type"] = "string"  # Replace 'anyOf' with AWS-supported format
                    field["nullable"] = True
                    del field["anyOf"]
    
    for path, methods in openapi_schema["paths"].items():
        for method, data in methods.items():
            if "operationId" in data:
                data["operationId"] = "".join(
                    word.capitalize() for word in data["operationId"].split("_")
                )  # Convert to CamelCase

    """"
    "openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
    }

    for path, methods in openapi_schema["paths"].items():
        if path != "/api/login":  # Skip authentication for login endpoint
            for method in methods:
                methods[method]["security"] = [{"BearerAuth": []}]"
    """

    # Ensure All Response Models Have `"type": "object"`
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        if "type" not in schema:
            schema["type"] = "object"  # Add type explicitly

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi