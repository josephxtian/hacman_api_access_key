from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_status():
    response = client.get("/v1/status/")
    assert response.status_code == 200
    assert response.json() == "API is online and working"