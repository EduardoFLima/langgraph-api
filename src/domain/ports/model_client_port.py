from abc import ABC, abstractmethod

class ModelClientPort(ABC):

    @abstractmethod
    def send_prompt(self, system_prompt: str, user_prompt: str, response_format: type) -> dict:
        raise NotImplementedError("send_prompt is not implemented")