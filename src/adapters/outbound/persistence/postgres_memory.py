from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from src.adapters.outbound.persistence.postgres_repository import PostgresStoreRepository
from src.application.ports.outbound.memory_port import MemoryPort


class PostgresMemory(MemoryPort):

    def __init__(self, db_uri: str):
        self._db_uri = db_uri

        self._checkpointer = None
        self._store = None

        self._checkpointer_context_manager = None
        self._store_context_manager = None

    def get_checkpointer(self):
        return self._checkpointer

    def get_store(self):
        return self._store

    async def start(self):
        self._checkpointer_context_manager = AsyncPostgresSaver.from_conn_string(self._db_uri)
        self._checkpointer = await self._checkpointer_context_manager.__aenter__()
        await self._checkpointer.setup()

        self._store_context_manager = PostgresStoreRepository.from_conn_string(self._db_uri)
        self._store = self._store_context_manager.__enter__()
        self._store.setup()

    async def stop(self):
        if self._checkpointer_context_manager:
            await self._checkpointer_context_manager.__aexit__(None, None, None)

        if self._store_context_manager:
            self._store_context_manager.__exit__(None, None, None)
