from src.domain.graph.graph import get_graph_definition
from src.domain.ports.model_client_port import ModelClientPort

def build_graph(model_client: ModelClientPort):
    return get_graph_definition(model_client)
