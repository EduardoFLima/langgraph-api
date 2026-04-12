from fastapi import Depends
from typing import Annotated

from src.adapters.outbound.model_clients.open_api_client import OpenAPIClient
from src.config import get_settings
from src.domain.graph.factory import build_graph
from src.domain.ports.chat_service_port import ChatServicePort
from src.domain.ports.model_client_port import ModelClientPort
from src.domain.services.chat_service import ChatService

from langgraph.graph.state import CompiledStateGraph


def get_model_client(settings=Depends(get_settings)) -> ModelClientPort:
    return OpenAPIClient(settings)


def get_graph(model_client=Depends(get_model_client)) -> CompiledStateGraph:
    return build_graph(model_client)


def get_chat_service(graph=Depends(get_graph)) -> ChatServicePort:
    return ChatService(graph)


ChatServiceDep = Annotated[ChatServicePort, Depends(get_chat_service)]
