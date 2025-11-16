from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_questions():
    response = client.get('/questions/')
    assert response.status_code in [200, 404]
    print(f"Status: {response.status_code}")