from typing import List

from fastapi import APIRouter, status, HTTPException

from src.adapters.inbound.api.schemas import (
    ItemResponse,
    ItemCreateRequest,
    ItemUpdateRequest,
)
from src.dependencies import ItemServiceDep

router = APIRouter(prefix="/items")


@router.get("/", response_model=list[ItemResponse])
def get_items(service: ItemServiceDep) -> List[ItemResponse]:
    items = service.getItems()
    return [ItemResponse.from_item(i) for i in items]


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, service: ItemServiceDep):
    item = service.getItem(item_id)

    if item is None:
        raise HTTPException(status_code=404)

    return ItemResponse.from_item(item)


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreateRequest, service: ItemServiceDep):
    item = service.createItem(item.name)
    return ItemResponse.from_item(item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item: ItemUpdateRequest, service: ItemServiceDep):
    item = service.updateItem(item.id, item.name)

    if item is None:
        raise HTTPException(status_code=404)

    return ItemResponse.from_item(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemServiceDep):
    service.deleteItem(item_id)
