from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    #Verifies the server can start and answer a basic request.
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.json()

    expected_keys = {
        "total_requests",
        "successful_requests", 
        "failed_requests", 
        "pending_requests", 
        "average_quality_score", 
        "pass_rate"
    }

    assert expected_keys.issubset(data.keys())

    assert isinstance(data["total_requests"], int)
    assert isinstance(data["average_quality_score"], float)

    #If DB is empty, pass_rate should be 0.0 (handling division by zero)
    if data["total_requests"] == 0:
        assert data["pass_rate"] == 0.0