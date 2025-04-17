from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel
from typing import List

from containers import Container
from repositories.items_repository import ItemsRepository

router = APIRouter(prefix="/api/locations", tags=["Locations"])

class ItemLocation(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

class ItemLocationResponse(BaseModel):
    items: List[ItemLocation]

@router.get("/items", response_model=ItemLocationResponse)
@inject
async def get_user_items_location(
    request: Request,
    items_repository_factory = Depends(Provide[Container.items_repository_factory])
):
    try:
        username = request.state.jwt_payload["sub"]
        items_repo: ItemsRepository = items_repository_factory()
        items = await items_repo.get_user_items(username=username)
        return ItemLocationResponse(
            items=[
                ItemLocation(
                    id=item.id,
                    name=item.name,
                    latitude=item.latitude,
                    longitude=item.longitude
                )
                for item in items
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")