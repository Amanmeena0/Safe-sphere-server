"""
Tests for service-layer logic using the in-memory database.
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, date

from app.services.user_service import UserService
from app.services.sos_service import SOSService
from app.schemas.user import UserUpdate
from app.schemas.sos import SOSReportCreate
from app.models.models import User


# =========================================================================
# UserService
# =========================================================================

class TestUserService:
    """Test UserService methods."""

    def test_get_or_create_returns_existing_user(self, db_session, test_user):
        """If the user already exists, return them without creating a duplicate."""
        service = UserService(db_session)
        result = service.get_or_create_user("test_clerk_user_123")
        assert result.id == test_user.id
        assert result.email == "test@example.com"

    def test_get_or_create_creates_new_user(self, db_session):
        """If the user doesn't exist, fetch from Clerk and create locally."""
        service = UserService(db_session)

        # Mock the Clerk API call to avoid real HTTP
        with patch.object(
            service,
            "_fetch_user_from_clerk",
            return_value={
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "Person",
            },
        ):
            result = service.get_or_create_user("brand_new_clerk_id")
            assert result.clerk_user_id == "brand_new_clerk_id"
            assert result.email == "new@example.com"
            assert result.name == "New Person"

    def test_get_profile_returns_user(self, db_session, test_user):
        service = UserService(db_session)
        result = service.get_profile("test_clerk_user_123")
        assert result.email == "test@example.com"

    def test_get_profile_not_found_raises(self, db_session):
        service = UserService(db_session)
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            service.get_profile("nonexistent_clerk_id")
        assert exc_info.value.status_code == 404

    def test_update_profile(self, db_session, test_user):
        service = UserService(db_session)
        update_data = UserUpdate(first_name="Updated", last_name="Name")
        result = service.update_profile("test_clerk_user_123", update_data)
        assert result.first_name == "Updated"
        assert result.last_name == "Name"

    def test_fetch_user_from_clerk_fallback_no_key(self, db_session):
        """Without CLERK_SECRET_KEY, _fetch_user_from_clerk returns fallback data."""
        service = UserService(db_session)
        with patch("app.services.user_service.settings") as mock_settings:
            mock_settings.CLERK_SECRET_KEY = None
            result = service._fetch_user_from_clerk("any_id")
            assert result["email"] == "unknown@example.com"
            assert result["first_name"] == "Clerk"


# =========================================================================
# SOSService
# =========================================================================

class TestSOSService:
    """Test SOSService methods."""

    def test_trigger_sos_creates_report(self, db_session, test_user):
        service = SOSService()
        sos_data = SOSReportCreate(
            location_address="123 Help St",
            latitude=28.6139,
            longitude=77.2090,
            incident_type="Robbery",
            description="Someone broke in",
        )
        result = service.trigger_sos(db_session, sos_data, "test_clerk_user_123")
        assert result.incident_type == "Robbery"
        assert result.clerk_user_id == "test_clerk_user_123"
        assert result.status == "active"

    def test_get_user_sos_reports_empty(self, db_session):
        service = SOSService()
        reports = service.get_user_sos_reports(db_session, "nonexistent_user")
        assert reports == []

    def test_get_user_sos_reports_after_trigger(self, db_session, test_user):
        service = SOSService()
        # Create a report first
        sos_data = SOSReportCreate(
            location_address="456 Alert Ave",
            latitude=19.0760,
            longitude=72.8777,
            incident_type="Accident",
        )
        service.trigger_sos(db_session, sos_data, "test_clerk_user_123")

        # Fetch it back
        reports = service.get_user_sos_reports(db_session, "test_clerk_user_123")
        assert len(reports) >= 1
        assert any(r["incident_type"] == "Accident" for r in reports)
