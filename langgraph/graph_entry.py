from src.adapters.outbound.persistence.postgres_memory import PostgresMemory
from src.adapters.outbound.model_clients.open_api_client import OpenAPIClient
from src.config import get_settings
from src.application.graph.factory import build_graph

_settings = get_settings()
_model_client = OpenAPIClient(_settings)
_memory_saver = PostgresMemory(_settings.memory.db_uri)

graph = build_graph(_model_client, _memory_saver)
