from abc import ABC, abstractmethod


class PathHistoryPort(ABC):

    @abstractmethod
    def store_path_to_history(self, user_id: str, path: str) -> None:
        raise NotImplementedError("store_path_to_history not implemented!")

    @abstractmethod
    def get_path_history(self, user_id: str) -> list[dict]:
        raise NotImplementedError("get_path_history not implemented!")

