from typing import Self

from pydantic import BaseModel

from src.domain.models.item import Item


class ItemCreateRequest(BaseModel):
    name: str


class ItemUpdateRequest(BaseModel):
    id: int
    name: str


class ItemResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_item(cls, item: Item) -> Self:
        return cls(
            id=item.id,
            name=item.name
        )