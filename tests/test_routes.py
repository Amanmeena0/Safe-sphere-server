"""
Tests for API routes using FastAPI TestClient.

Auth is mocked via conftest.py fixtures so we can test route logic
without Clerk, PostgreSQL, or Redis running.
"""
import pytest


# =========================================================================
# General / Health-check route
# =========================================================================

class TestHelloRoute:
    """Test the root health-check endpoint."""

    def test_hello_world(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Safe-sphere" in data["message"]


# =========================================================================
# Profile routes
# =========================================================================

class TestProfileRoutes:
    """Test /api/profile endpoints."""

    def test_get_my_profile(self, client):
        response = client.get("/api/profile/me")
        assert response.status_code == 200
        data = response.json()
        assert data["clerk_user_id"] == "test_clerk_user_123"
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"

    def test_get_my_firs_empty(self, client):
        """A new user should have no FIR reports."""
        response = client.get("/api/profile/firs")
        assert response.status_code == 200
        data = response.json()
        # All FIR categories should be present but empty
        assert "cyber_crimes" in data
        assert "lost_items" in data
        assert "missing_persons" in data
        assert isinstance(data["cyber_crimes"], list)
        assert len(data["cyber_crimes"]) == 0


# =========================================================================
# SOS routes
# =========================================================================

class TestSOSRoutes:
    """Test /api/sos endpoints."""

    def test_trigger_sos_success(self, client):
        payload = {
            "location_address": "123 Emergency Rd, Delhi",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "incident_type": "Fire",
            "description": "Building on fire, people trapped",
        }
        response = client.post("/api/sos/trigger", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["incident_type"] == "Fire"
        assert data["clerk_user_id"] == "test_clerk_user_123"
        assert data["status"] == "active"

    def test_trigger_sos_invalid_latitude(self, client):
        payload = {
            "location_address": "Bad place",
            "latitude": 999.0,  # invalid
            "longitude": 77.0,
            "incident_type": "Test",
        }
        response = client.post("/api/sos/trigger", json=payload)
        assert response.status_code == 422  # Pydantic validation error

    def test_trigger_sos_missing_required_fields(self, client):
        payload = {
            "latitude": 28.0,
            "longitude": 77.0,
            # missing location_address and incident_type
        }
        response = client.post("/api/sos/trigger", json=payload)
        assert response.status_code == 422


# =========================================================================
# Auth guard — unauthenticated requests
# =========================================================================

class TestAuthGuard:
    """Verify that protected endpoints reject unauthenticated requests."""

    def test_profile_me_requires_auth(self, unauthenticated_client):
        response = unauthenticated_client.get("/api/profile/me")
        assert response.status_code in (401, 403)  # HTTPBearer rejects missing tokens

    def test_sos_trigger_requires_auth(self, unauthenticated_client):
        payload = {
            "location_address": "Test",
            "latitude": 28.0,
            "longitude": 77.0,
            "incident_type": "Test",
        }
        response = unauthenticated_client.post("/api/sos/trigger", json=payload)
        assert response.status_code in (401, 403)
