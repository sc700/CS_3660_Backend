from fastapi import APIRouter, HTTPException
from repositories.items_repository import get_location_history

router = APIRouter(prefix="/api/location-history", tags=["Location History"])

@router.get("/users/{username}")
async def get_location_history_endpoint(username: str):
    history = get_location_history(username)
    return {"history": history}