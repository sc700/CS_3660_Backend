import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import login_controller,items_api_controller, locations_controller, location_history_controller, account_details_controller, signup_api_controller
from middleware.middleware import AuthMiddleware
from schemas.message_schema import MessageResponse

app = FastAPI(title="CS3660 Backend Project", version="1.0.0")

app.add_middleware(
    AuthMiddleware,
    public_paths=["/", "/home", "/api/login", "/favicon.ico", "/about", "/signup"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_controller.router)
app.include_router(items_api_controller.router)
app.include_router(locations_controller.router)
app.include_router(location_history_controller.router)
app.include_router(account_details_controller.router)
#app.include_router(access_control_controller.router)
app.include_router(signup_api_controller.router)

@app.get("/", response_model=MessageResponse)
def read_root():
    return {"message": "Backend is running!"}

@app.get("/health", response_model=MessageResponse)
def health():
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)