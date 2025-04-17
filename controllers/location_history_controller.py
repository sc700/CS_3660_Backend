from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel
from typing import List

from containers import Container
from repositories.items_repository import ItemsRepository

router = APIRouter(prefix="/api/location-history", tags=["LocationHistory"])

class ItemLocation(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

class ItemLocationResponse(BaseModel):
    items: List[ItemLocation]

@router.get("/users/{username}/items", response_model=ItemLocationResponse)
@inject
async def get_user_items_location_history(
    username: str,
    items_repository_factory=Depends(Provide[Container.items_repository_factory])
):
    try:
        items_repo: ItemsRepository = items_repository_factory()
        items = await items_repo.get_user_items(username=username)

        item_list = [
            ItemLocation(
                id=item.id,
                name=item.name,
                latitude=item.latitude,
                longitude=item.longitude
            )
            for item in items
        ]

        return ItemLocationResponse(items=item_list)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching location history: {str(e)}")    