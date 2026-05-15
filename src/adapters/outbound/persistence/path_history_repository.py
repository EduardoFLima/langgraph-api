from datetime import datetime, timezone

import psycopg

from src.application.ports.outbound.path_history_port import PathHistoryPort


class PathHistoryRepository(PathHistoryPort):

    def __init__(self, db_uri: str):
        self._db_uri = db_uri
        self._conn = None

    def connect(self):
        self._conn = psycopg.connect(self._db_uri)
        self._setup()

    def _setup(self):
        with self._conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS path_history (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    path VARCHAR(255) NOT NULL,
                    saved_at TIMESTAMP WITH TIME ZONE NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_path_history_user_id ON path_history(user_id);
            """)
            self._conn.commit()

    def store_path_to_history(self, user_id: str, path: str) -> None:
        timestamp = datetime.now(timezone.utc)
        with self._conn.cursor() as cur:
            cur.execute(
                "INSERT INTO path_history (user_id, path, saved_at) VALUES (%s, %s, %s)",
                (user_id, path, timestamp),
            )
            self._conn.commit()

    def get_path_history(self, user_id: str) -> list[dict]:
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT path, saved_at FROM path_history WHERE user_id = %s ORDER BY saved_at DESC LIMIT 100",
                (user_id,),
            )
            rows = cur.fetchall()
            return [{"path": row[0], "saved_at": row[1].isoformat()} for row in rows]

    def close(self):
        if self._conn:
            self._conn.close()

