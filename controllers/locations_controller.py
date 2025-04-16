from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependency_injector.wiring import inject, Provide

from containers import Container
from repositories.items_repository import ItemsRepository
from database.db import get_async_db

router = APIRouter(prefix="/api/locations", tags=["Locations"])

@router.get("/users/{username}/items")
@inject
async def get_user_items_location(
    username: str,
    db: AsyncSession = Depends(get_async_db),
    items_repo: ItemsRepository = Depends(Provide[Container.items_repository])
):
    try:
        items = await items_repo.get_user_items(db, username)
        return {"items": [
            {
                "id": item.id,
                "name": item.name,
                "latitude": item.latitude,
                "longitude": item.longitude
            }
            for item in items
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")