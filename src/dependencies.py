from fastapi import Depends
from typing import Annotated

from src.adapters.outbound.persistence.in_memory_item_repository import (
    InMemoryItemRepository,
)
from src.domain.ports.item_repository_port import ItemRepositoryPort
from src.domain.ports.item_service_port import ItemServicePort
from src.domain.services.item_service import ItemService

_item_repository = InMemoryItemRepository()

def get_item_repository() -> ItemRepositoryPort:
    return _item_repository


def get_item_service(
    repository: Annotated[ItemRepositoryPort, Depends(get_item_repository)],
) -> ItemServicePort:
    return ItemService(repository=repository)


ItemServiceDep = Annotated[ItemServicePort, Depends(get_item_service)]
