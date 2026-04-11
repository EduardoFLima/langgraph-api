from abc import ABC, abstractmethod
from typing import Final, List

from src.domain.models.item import Item

NOT_IMPLEMENTED_ERROR_MSG: Final = "Method not implemented"

class ItemServicePort(ABC):

    @abstractmethod
    def getItems(self) -> list[Item]:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def getItem(self, id: int) -> Item:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def createItem(self, name: str) -> Item:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def updateItem(self, id: int, name: str) -> Item:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def deleteItem(self, id: int) -> None:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)
