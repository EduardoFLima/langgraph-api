from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat():
    response = client.post("/chat", json={"question": "how are u?"})
    assert response.status_code == 200

    print(f"response: {response.json()}")
