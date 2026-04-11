from typing import List, Self

from src.domain.models.item import Item
from src.domain.ports.item_repository_port import ItemRepositoryPort
from src.domain.ports.item_service_port import ItemServicePort


class ItemService(ItemServicePort):

    def __init__(self, repository: ItemRepositoryPort) -> Self:
        self._repository = repository

    def getItems(self) -> list[Item]:
        return list(
            self._repository.get_all().values()
        )

    def getItem(self, id: int) -> Item:
        return self._repository.get_by_id(id)

    def createItem(self, name: str) -> Item:
        return self._repository.create(Item(id=None, name=name))

    def updateItem(self, id: int, name: str) -> Item | None:
        return self._repository.update(Item(id, name))

    def deleteItem(self, id: int) -> None:
        self._repository.delete(id)
