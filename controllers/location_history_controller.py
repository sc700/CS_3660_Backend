from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from containers import Container
from repositories.items_repository import ItemsRepository

router = APIRouter(prefix="/api/location-history", tags=["LocationHistory"])

@router.get("/users/{username}/items")
@inject
async def get_user_items_location_history(
    username: str,
    items_repository_factory = Depends(Provide[Container.items_repository_factory])
):
    try:
        items_repo: ItemsRepository = items_repository_factory()
        items = await items_repo.get_user_items(username=username)
        return {
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "latitude": item.latitude,
                    "longitude": item.longitude
                }
                for item in items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching location history: {str(e)}")