from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject

from containers import Container
from services.items_api_service import ItemsAPIService
from schemas.items_schema import ItemSchema, ItemListResponse, ItemCreateRequest
from schemas.message_schema import MessageResponse

router = APIRouter(prefix="/api/items", tags=["Items"])


@router.get("/items", response_model=ItemListResponse)
@inject
async def get_items(
    request: Request,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    username = request.state.jwt_payload["sub"]
    return await items_service.get_user_items(username=username)


@router.post("", response_model=ItemSchema)
@inject
async def add_item(
    request: Request,
    item: ItemCreateRequest,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    username = request.state.jwt_payload["sub"]
    return await items_service.add_user_item(username, item.dict())


@router.put("/{item_id}", response_model=ItemSchema)
@inject
async def update_item(
    item_id: int,
    item: ItemCreateRequest,
    request: Request,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    username = request.state.jwt_payload["sub"]
    return await items_service.update_user_item(username, item_id, item.dict())


@router.delete("/{item_id}", response_model=MessageResponse)
@inject
async def delete_item(
    item_id: int,
    request: Request,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    username = request.state.jwt_payload["sub"]
    success = await items_service.delete_user_item(username, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return MessageResponse(message="Item deleted successfully")