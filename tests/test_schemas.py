"""
Tests for Pydantic schemas — validation, defaults, and edge cases.
"""
import pytest
from datetime import datetime, date
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.fir import (
    LostItemCreate,
    CyberCrimeCreate,
    TheftEfirCreate,
    MissingPersonCreate,
)
from app.schemas.sos import SOSReportCreate, SOSReportResponse


# =========================================================================
# User schemas
# =========================================================================

class TestUserCreate:
    """Validate UserCreate schema."""

    def test_valid_user_create(self):
        user = UserCreate(
            clerk_user_id="clerk_abc123",
            email="alice@example.com",
            first_name="Alice",
            last_name="Smith",
            name="Alice Smith",
        )
        assert user.clerk_user_id == "clerk_abc123"
        assert user.email == "alice@example.com"

    def test_user_create_requires_clerk_id(self):
        with pytest.raises(ValidationError):
            UserCreate(email="nobody@example.com")

    def test_user_create_optional_fields(self):
        user = UserCreate(clerk_user_id="clerk_xyz")
        assert user.email is None
        assert user.first_name is None
        assert user.last_name is None
        assert user.name is None

    def test_user_create_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(clerk_user_id="clerk_xyz", email="not-an-email")


class TestUserUpdate:
    """Validate UserUpdate schema."""

    def test_all_fields_optional(self):
        update = UserUpdate()
        assert update.email is None
        assert update.first_name is None

    def test_partial_update(self):
        update = UserUpdate(first_name="NewName")
        assert update.first_name == "NewName"
        assert update.email is None

    def test_invalid_email_rejected(self):
        with pytest.raises(ValidationError):
            UserUpdate(email="bad-email")


# =========================================================================
# FIR schemas
# =========================================================================

class TestLostItemCreate:
    """Validate LostItemCreate schema."""

    def test_valid_lost_item(self):
        item = LostItemCreate(
            police_station="Central PS",
            item_name="Laptop",
            placeofloss="Market",
            loss_datetime=datetime(2024, 1, 15, 10, 30),
            owner_name="John Doe",
            contact_number="9876543210",
            document_type="Electronics",
            district="Downtown",
        )
        assert item.item_name == "Laptop"
        assert item.brand is None  # optional field

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            LostItemCreate(police_station="Central PS")

    def test_optional_brand_and_model(self):
        item = LostItemCreate(
            police_station="Central PS",
            item_name="Phone",
            brand="Apple",
            model="iPhone 15",
            placeofloss="Bus Stop",
            loss_datetime=datetime(2024, 6, 1),
            owner_name="Jane",
            contact_number="1234567890",
            document_type="Mobile",
            district="East",
        )
        assert item.brand == "Apple"
        assert item.model == "iPhone 15"


class TestCyberCrimeCreate:
    """Validate CyberCrimeCreate schema."""

    def test_valid_cyber_crime(self):
        crime = CyberCrimeCreate(
            police_station="Cyber PS",
            crimeCategory="Phishing",
            date_of_incident=date(2024, 3, 20),
            description="Received a phishing email leading to credential theft.",
            full_name="Bob Marley",
            contact_number="5551234567",
            address="123 Main St",
        )
        assert crime.crimeCategory == "Phishing"
        assert crime.digitalEvidence == ""  # default

    def test_missing_description_rejected(self):
        with pytest.raises(ValidationError):
            CyberCrimeCreate(
                police_station="Cyber PS",
                crimeCategory="Fraud",
                date_of_incident=date(2024, 1, 1),
                full_name="Someone",
                contact_number="0000000000",
                address="Somewhere",
                # description intentionally missing
            )


class TestTheftEfirCreate:
    """Validate TheftEfirCreate schema."""

    def test_valid_theft_efir(self):
        efir = TheftEfirCreate(
            police_station="North PS",
            incident_description="Bike stolen from parking lot",
            date_of_theft=date(2024, 5, 10),
        )
        assert efir.financial_impact is None
        assert efir.upload_document == ""

    def test_missing_incident_description(self):
        with pytest.raises(ValidationError):
            TheftEfirCreate(
                police_station="North PS",
                date_of_theft=date(2024, 5, 10),
            )


class TestMissingPersonCreate:
    """Validate MissingPersonCreate schema."""

    def test_valid_missing_person(self):
        mp = MissingPersonCreate(
            police_station="South PS",
            Fullname="John Doe",
            Numberofperson=1,
            nickname="JD",
            fathername="Richard Doe",
            relation="Son",
            lastknownlocation="Central Park",
            yearofbirth=2000,
            agefrom=24,
            ageto=24,
            bodybuild="Medium",
            complexion="Fair",
            weight=70.0,
            height=175.0,
            incidentReport="Last seen walking towards the east exit.",
            detailsLastseen="Wearing blue jeans and white shirt",
            datetimelastseen=datetime(2024, 6, 15, 18, 30),
            complainant_name="Richard Doe",
            relationwithMissingperson="Father",
            complainant_address="456 Oak Ave",
            complainant_contact="9998887776",
            alternate_contact="1112223334",
            emailaddress="richard@example.com",
            anyotherdetails="Has a scar on left hand",
            district="South",
        )
        assert mp.Fullname == "John Doe"
        assert mp.weight == 70.0


# =========================================================================
# SOS schemas
# =========================================================================

class TestSOSReportCreate:
    """Validate SOSReportCreate schema."""

    def test_valid_sos_report(self):
        sos = SOSReportCreate(
            location_address="123 Emergency Rd",
            latitude=28.6139,
            longitude=77.2090,
            incident_type="Fire",
            description="Building on fire, need help",
        )
        assert sos.latitude == 28.6139

    def test_description_optional(self):
        sos = SOSReportCreate(
            location_address="456 Help St",
            latitude=19.0760,
            longitude=72.8777,
            incident_type="Accident",
        )
        assert sos.description is None

    def test_latitude_out_of_range(self):
        with pytest.raises(ValidationError):
            SOSReportCreate(
                location_address="Bad Location",
                latitude=100.0,  # > 90
                longitude=77.0,
                incident_type="Test",
            )

    def test_longitude_out_of_range(self):
        with pytest.raises(ValidationError):
            SOSReportCreate(
                location_address="Bad Location",
                latitude=28.0,
                longitude=200.0,  # > 180
                incident_type="Test",
            )

    def test_missing_incident_type(self):
        with pytest.raises(ValidationError):
            SOSReportCreate(
                location_address="Some Place",
                latitude=28.0,
                longitude=77.0,
                # incident_type missing
            )
