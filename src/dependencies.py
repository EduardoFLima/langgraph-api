from typing import Annotated

from fastapi import Depends
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph

from application.services.tools_service import get_all_mcp_tools
from src.adapters.outbound.model_clients.open_api_client import OpenAPIClient
from src.adapters.outbound.persistence.path_history_repository import PathHistoryRepository
from src.adapters.outbound.persistence.postgres_memory import PostgresMemory
from src.application.graph.factory import build_graph
from src.application.ports.inbound.chat_use_case import ChatUseCase
from src.application.ports.outbound.memory_port import MemoryPort
from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.ports.outbound.path_history_port import PathHistoryPort
from src.application.services.chat_service import ChatService
from src.config import get_settings


def get_model_client(settings=Depends(get_settings)) -> ModelClientPort:
    return OpenAPIClient(settings)


async def get_postgres_memory(settings=Depends(get_settings)) -> MemoryPort:
    memory = PostgresMemory(settings.memory.db_uri)
    await memory.start()
    return memory


def get_path_history_repository(settings=Depends(get_settings)) -> PathHistoryPort:
    repo = PathHistoryRepository(settings.path_history.db_uri)
    repo.connect()
    return repo


async def get_mcp_tools(settings=Depends(get_settings), path_history_repo=Depends(get_path_history_repository)) -> list[BaseTool]:
    return await get_all_mcp_tools(settings.reports_dir, path_history_repo)

async def get_graph(
        settings=Depends(get_settings),
        model_client=Depends(get_model_client),
        memory_saver=Depends(get_postgres_memory),
        path_history_repo=Depends(get_path_history_repository),
        tools=Depends(get_mcp_tools)
) -> CompiledStateGraph:
    return build_graph(settings, model_client, memory_saver, path_history_repo, tools)


async def get_chat_service(graph=Depends(get_graph)) -> ChatUseCase:
    return ChatService(graph)


ChatServiceDep = Annotated[ChatUseCase, Depends(get_chat_service)]
