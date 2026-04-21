import pytest
from httpx import Response
from starlette.testclient import TestClient

from src.main import app


def send_message_to_chat(client: TestClient, message: str) -> Response:
    response = client.post("/chat", json={"question": message})

    assert response.status_code == 200
    assert response.json() is not None
    assert response.cookies is not None

    return response


class TestChatPersistence:

    @pytest.fixture()
    def client(self):
        return TestClient(app)

    def test_graph_should_make_a_summary_after_hitting_the_threshold(self, client):
        response = send_message_to_chat(client, "how are u? I just want to go fast, first choice!")

        path = response.json().get("path")
        assert path == "path_a"
        thread_id = response.cookies.get("thread_id")

        send_message_to_chat(client, "this is fun!")
        response = send_message_to_chat(client, "what path did I take previously?")

        messages = response.json().get("messages")
        assert messages is not None
        assert len(messages) == 6

        send_message_to_chat(client, "ah ! thank you")
        send_message_to_chat(client, "what if i take another path?")
        response = send_message_to_chat(client, "You are very smart. Take the path I did previously!")

        path = response.json().get("path")
        assert path == "path_a"
        assert thread_id == response.cookies.get("thread_id")
        messages = response.json().get("messages")
        assert messages is not None
        assert len(messages) == 6
