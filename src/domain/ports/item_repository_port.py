from abc import ABC, abstractmethod
from typing import Final, List

from src.domain.models.item import Item

NOT_IMPLEMENTED_ERROR_MSG: Final = "Method not implemented"


class ItemRepositoryPort(ABC):

    @abstractmethod
    def get_all(self) -> dict[int, Item]:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def get_by_id(self, id: int) -> Item | None:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def create(self, item: Item) -> Item:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def update(self, item: Item) -> Item | None:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def delete(self, id: int) -> bool:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)
