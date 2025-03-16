from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze():
    response = client.post("/analyze", json={"function_code": "def add(a, b): return a + b"})
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
