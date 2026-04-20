import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.application.graph.graph_state import Path
from src.main import app
from src.adapters.outbound.persistence.postgres_memory import PostgresMemory


class TestChatPersistence:

    @pytest.fixture()
    def client(self):
        return TestClient(app)

    def test_graph_should_remember_previous_path(self, client):
        thread_id = "test_graph_should_remember_previous_path" + str(datetime.now())
        # first call
        client.cookies.set("thread_id", thread_id)
        response = client.post("/chat", json={"question": "how are u? I just want to go fast, first choice!"})
        assert response.status_code == 200
        assert response.json() is not None

        path = response.json().get("path")
        assert path == "path_a"

        # the second call should remember the path
        client.cookies.set("thread_id", thread_id)
        response = client.post("/chat", json={"question": "how are u? what path did I take previously?"})
        assert response.status_code == 200
        assert response.json() is not None

        path = response.json().get("path")
        assert path == "path_a"

    def test_graph_should_keep_memory_when_thread_id_is_not_given(self, client):
        # first call
        response = client.post("/chat", json={"question": "how are u? Im skeptical, i want a second path!"})
        assert response.status_code == 200

        assert response.json() is not None
        path = response.json().get("path")
        assert path == "path_b"

        assert response.cookies is not None
        thread_id = response.cookies.get("thread_id")

        # the second call should remember the path and return the thread id
        client.cookies.set("thread_id", thread_id)
        response = client.post("/chat", json={"question": "how are u? what path did I take? "})
        assert response.status_code == 200
        assert response.json() is not None

        path = response.json().get("path")
        assert path == "path_b"

        assert response.cookies is not None
        assert response.cookies.get("thread_id") == thread_id

    def test_graph_should_load_path_preferences_from_store(self, client):
        user_id = str(uuid.uuid4())

        memory = PostgresMemory(dbUri="postgresql://postgres:somepassword@localhost:5432/some_db")
        store = memory.get_store()
        store.put(
            namespace=("preferences", "paths"),
            key=user_id,
            value={"preferred_path": Path.PATH_B.value}
        )

        response = client.post(f"/chat?user_id={user_id}", json={"question": "how are u? what path do u think i like ?"})
        assert response.status_code == 200
        assert response.json() is not None

        path = response.json().get("path")
        assert path == "path_b"