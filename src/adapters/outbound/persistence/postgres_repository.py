from datetime import datetime, timezone

from langgraph.store.base import SearchItem
from langgraph.store.postgres import PostgresStore


class PostgresStoreRepository(PostgresStore):

    def get_preferred_path(self, user_id):
        return self.get(namespace=("preferences", "paths"), key=user_id)

    def save_preferred_path(self, user_id, preferred_path):
        self.put(
            namespace=("preferences", "paths"),
            key=user_id,
            value={"preferred_path": preferred_path},
        )

    ### IMPORTANT: this is a workaround. For serious reporting, this needs to be treated in a separated database ###
    ### [START] ###

    def store_path_to_history(self, user_id, path):
        timestamp = datetime.now(timezone.utc).isoformat()
        self.put(
            namespace=("history", "path", user_id),
            key=timestamp,
            value={"path": path, "saved_at": timestamp},
        )

    def get_path_history(self, user_id: str) -> list[SearchItem]:
        return self.search(("history", "path", user_id), limit=100)

    ### [END] ###
