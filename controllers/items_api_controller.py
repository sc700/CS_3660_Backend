from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession
from containers import Container
from services.items_api_service import ItemsAPIService
from database.db import get_async_db
from schemas.items_schema import ItemSchema, ItemListResponse, ItemCreateRequest

router = APIRouter(prefix="/api/items", tags=["Items"])

@router.get("/{username}", response_model=ItemListResponse)
@inject
async def get_items(
    username: str,
    db: AsyncSession = Depends(get_async_db),
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return await items_service.get_user_items(db, username)

@router.post("/{username}", response_model=ItemSchema)
@inject
async def add_item(
    username: str,
    item: ItemCreateRequest,
    db: AsyncSession = Depends(get_async_db),
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return await items_service.add_user_item(db, username, item.dict())

@router.put("/{username}/{item_id}", response_model=ItemSchema)
@inject
async def update_item(
    username: str,
    item_id: int,
    item: ItemCreateRequest,
    db: AsyncSession = Depends(get_async_db),
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return await items_service.update_user_item(db, username, item_id, item.dict())

@router.delete("/{username}/{item_id}")
@inject
async def delete_item(
    username: str,
    item_id: int,
    db: AsyncSession = Depends(get_async_db),
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    success = await items_service.delete_user_item(db, username, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True}