from langchain_core.tools import BaseTool

from src.application.graph.graph import get_graph_definition
from src.application.ports.outbound.memory_port import MemoryPort
from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.ports.outbound.path_history_port import PathHistoryPort
from src.config import Settings


def build_graph(settings: Settings, model_client: ModelClientPort, memory_saver: MemoryPort, path_history_repo: PathHistoryPort, tools: list[BaseTool]):
    return get_graph_definition(settings, model_client, memory_saver, path_history_repo, tools)
