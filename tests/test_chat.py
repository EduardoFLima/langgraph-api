import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_graph_going_through_path_a(client):
    client.cookies.set("thread_id", "test_graph_going_through_path_a")
    response = client.post("/chat", json={"question": "how are u? I just want to go fast, first choice!"})
    assert response.status_code == 200
    assert response.json() is not None

    scenario = response.json().get("scenario")
    assert scenario == "path_a_scenario"

def test_graph_going_through_path_b(client):
    client.cookies.set("thread_id", "test_graph_going_through_path_b")
    response = client.post("/chat", json={"question": "Im looking for altenratives..."})
    assert response.status_code == 200
    assert response.json() is not None

    scenario = response.json().get("scenario")
    assert scenario == "path_b_scenario"

def test_graph_going_through_path_unknown(client):
    client.cookies.set("thread_id", "test_graph_going_through_path_unknown")
    response = client.post("/chat", json={"question": "I want to order food."})
    assert response.status_code == 200
    assert response.json() is not None

    scenario = response.json().get("scenario")
    assert scenario == "unknown_scenario"

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
