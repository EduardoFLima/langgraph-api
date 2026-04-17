from src.application.ports.memory_port import MemoryPort
from src.application.graph.graph import get_graph_definition
from src.application.ports.model_client_port import ModelClientPort

def build_graph(model_client: ModelClientPort, memory_saver: MemoryPort):
    return get_graph_definition(model_client, memory_saver)