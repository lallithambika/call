from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_missing_api_key_returns_401() -> None:
    response = client.post(
        "/api/call-analytics",
        json={
            "language": "Tamil",
            "audioFormat": "mp3",
            "audioBase64": "dGVzdA==dGVzdA==dGVzdA==dGVzdA==dGVzdA==",
        },
    )
    assert response.status_code == 401
