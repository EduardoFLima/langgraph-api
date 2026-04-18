import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_graph_should_remember_previous_path(client):
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
