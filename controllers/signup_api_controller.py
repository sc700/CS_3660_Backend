from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from containers import Container
from repositories.user_repository import UserRepository
from schemas.message_schema import MessageResponse

router = APIRouter(prefix="/api", tags=["Authentication"])

class SignUpRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
@inject
def signup(
    signup_request: SignUpRequest,
    user_repository: UserRepository = Depends(Provide[Container.user_repository])
):
    try:
        user_repository.add_user(signup_request.dict())
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User creation failed: {e}")