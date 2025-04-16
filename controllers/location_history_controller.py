from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_db
from repositories.items_repository import ItemsRepository

router = APIRouter(prefix="/api/location-history", tags=["Location History"])

@router.get("/users/{username}")
async def get_location_history_endpoint(
    username: str,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        history = await ItemsRepository.get_location_history(db, username)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving history: {e}")