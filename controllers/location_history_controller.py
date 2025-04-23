from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel
from typing import List

from containers import Container
from repositories.items_repository import ItemsRepository

#/api/location-history/users/${user.username}

router = APIRouter(prefix="/api/location-history", tags=["LocationHistory"])

class ItemLocation(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

class ItemLocationResponse(BaseModel):
    items: List[ItemLocation]


@router.get("/users/{username}", response_model=ItemLocationResponse)
@inject
def get_user_items_location_history(
    username: str,
    items_repository: ItemsRepository = Depends(Provide[Container.items_repository])
):
    try:
        items = items_repository.get_user_items(username=username)

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