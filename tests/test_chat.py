from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat():
    response = client.post("/chat", json={"question": "how are u? I just want to go fast, first choice!"})
    assert response.status_code == 200
    assert response.json() is not None

    answer = response.json().get("answer")
    assert answer is not None

    assert "path_a" in answer

def test_chat():
    response = client.post("/chat", json={"question": "Im looking for altenratives..."})
    assert response.status_code == 200
    assert response.json() is not None

    answer = response.json().get("answer")
    assert answer is not None

    assert "path_b" in answer
