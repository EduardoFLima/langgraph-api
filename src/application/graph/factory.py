from langchain_core.tools import BaseTool

from config import Settings
from src.application.graph.graph import get_graph_definition
from src.application.ports.outbound.memory_port import MemoryPort
from src.application.ports.outbound.model_client_port import ModelClientPort


def build_graph(settings: Settings, model_client: ModelClientPort, memory_saver: MemoryPort, tools: list[BaseTool]):
    return get_graph_definition(settings, model_client, memory_saver, tools)