from abc import ABC, abstractmethod

class ModelClientPort(ABC):

    @abstractmethod
    def send_prompt(self, prompt: str) -> dict:
        raise NotImplementedError("send_prompt is not implemented")