from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import Provide, inject

from containers import Container
from services.items_api_service import ItemsAPIService
from schemas.items_schema import ItemSchema, ItemListResponse, ItemCreateRequest

router = APIRouter(prefix="/api/items", tags=["Items"])

@router.get("/items", response_model=ItemListResponse)
@inject
async def get_items(
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return await items_service.get_user_items(username="admin@admin")  # placeholder

@router.post("/{username}", response_model=ItemSchema)
@inject
async def add_item(
    username: str,
    item: ItemCreateRequest,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return await items_service.add_user_item(username, item.dict())

@router.put("/{username}/{item_id}", response_model=ItemSchema)
@inject
async def update_item(
    username: str,
    item_id: int,
    item: ItemCreateRequest,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return await items_service.update_user_item(username, item_id, item.dict())

@router.delete("/{username}/{item_id}")
@inject
async def delete_item(
    username: str,
    item_id: int,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    success = await items_service.delete_user_item(username, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True}