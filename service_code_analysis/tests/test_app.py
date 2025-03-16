from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_start():
    response = client.post("/analyze/start", json={"repo_url": "https://github.com/Python-World/python-mini-projects"})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
