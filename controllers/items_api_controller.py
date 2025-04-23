from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject

from containers import Container
from services.items_api_service import ItemsAPIService
from schemas.items_schema import ItemSchema, ItemListResponse, ItemCreateRequest
from schemas.message_schema import MessageResponse

router = APIRouter(prefix="/api/items", tags=["Items"])


@router.get("/items", response_model=ItemListResponse)
@inject
def get_user_items(
    request: Request,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    username = request.state.jwt_payload["sub"]
    return items_service.get_user_items(username)


#`/api/items/users/${user.username}/items`
@router.post("/items", response_model=ItemSchema)
@inject
def add_item(
    item: ItemCreateRequest,
    request: Request,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    username = request.state.jwt_payload["sub"]
    return items_service.add_user_item(username, item.dict())


@router.put("/users/{username}/items/{item_id}", response_model=ItemSchema)
@inject
def update_item(
    username: str,
    item_id: int,
    item: ItemCreateRequest,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    return items_service.update_user_item(username, item_id, item.dict())



@router.delete("/users/{username}/items/{item_id}", response_model=MessageResponse)
@inject
def delete_item(
    username: str,
    item_id: int,
    items_service: ItemsAPIService = Depends(Provide[Container.items_api_service])
):
    success = items_service.delete_user_item(username, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return MessageResponse(message="Item deleted successfully")
