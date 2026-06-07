import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_fastapi_health():
    """Smoke test to ensure FastAPI app is importable and responsive."""
    # Note: We need to define a root or health endpoint if it doesn't exist
    # For now, let's just check if we can get a 404 or something else than a 500
    response = client.get("/")
    assert response.status_code in [200, 404]

