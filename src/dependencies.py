from fastapi import Depends
from typing import Annotated

from src.domain.ports.chat_service_port import ChatServicePort
from src.domain.services.chat_service import ChatService


def get_chat_service() -> ChatServicePort:
    return ChatService()


ChatServiceDep = Annotated[ChatServicePort, Depends(get_chat_service)]
