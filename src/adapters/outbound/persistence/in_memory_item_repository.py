from typing import List

from src.domain.models.item import Item
from src.domain.ports.item_repository_port import ItemRepositoryPort


class InMemoryItemRepository(ItemRepositoryPort):
    def __init__(self):
        self._next_id = 1
        default_item = Item(id=self._next_id, name="some item")

        self._items: dict[int, Item] = {default_item.id: default_item}

    def get_all(self) -> dict[int, Item]:
        return self._items

    def get_by_id(self, id: int) -> Item | None:
        return self._items.get(id)

    def create(self, item: Item) -> Item:
        self._next_id += 1
        item.id = self._next_id
        self._items[item.id] = item
        return self._items[item.id]

    def update(self, item: Item) -> Item | None:
        if item.id is None:
            raise RuntimeError("Item does not has an ID. It cannot be updated")

        if self._items.get(item.id) is None:
            return None

        self._items[item.id] = item

        return self._items[item.id]

    def delete(self, id: int) -> bool:
        if id in self._items:
            del self._items[id]
            return True

        return False
