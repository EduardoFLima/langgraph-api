from abc import ABC, abstractmethod

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.store.base import BaseStore


class MemoryPort(ABC):

    @abstractmethod
    def get_checkpointer(self) -> BaseCheckpointSaver:
        raise NotImplementedError("get_checkpointer not implemented!")

    @abstractmethod
    def get_store(self) -> BaseStore:
        raise NotImplementedError("get_store not implemented!")

    @abstractmethod
    async def start(self):
        raise NotImplementedError("start not implemented!")

    @abstractmethod
    async def stop(self):
        raise NotImplementedError("stop not implemented!")

