import pytest
from fastapi.testclient import TestClient
from src.main import app


class TestChatPersitence:

    @pytest.fixture(scope="module")
    def client(self):
        return TestClient(app)

    def test_graph_should_remember_previous_path(self, client):
        # first call
        client.cookies.set("thread_id", "test_graph_should_remember_previous_path")
        response = client.post("/chat", json={"question": "how are u? I just want to go fast, first choice!"})
        assert response.status_code == 200
        assert response.json() is not None

        scenario = response.json().get("scenario")
        assert scenario == "path_a_scenario"

        # the second call should remember the path
        client.cookies.set("thread_id", "test_graph_should_remember_previous_path")
        response = client.post("/chat", json={"question": "how are u? what path did I take?"})
        assert response.status_code == 200
        assert response.json() is not None

        scenario = response.json().get("scenario")
        assert scenario == "path_a_scenario"

    def test_graph_should_keep_memory_when_thread_id_is_not_given(self, client):
        # first call
        response = client.post("/chat", json={"question": "how are u? Im skeptical, i want a second path!"})
        assert response.status_code == 200

        assert response.json() is not None
        scenario = response.json().get("scenario")
        assert scenario == "path_b_scenario"

        assert response.cookies is not None
        thread_id = response.cookies.get("thread_id")

        # the second call should remember the path and return the thread id
        client.cookies.set("thread_id", thread_id)
        response = client.post("/chat", json={"question": "how are u? what path did I take? "})
        assert response.status_code == 200
        assert response.json() is not None

        scenario = response.json().get("scenario")
        assert scenario == "path_b_scenario"

        assert response.cookies is not None
        assert response.cookies.get("thread_id") == thread_id
