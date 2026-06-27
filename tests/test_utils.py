"""
Tests for utility modules — date_utils and errors.
"""
import pytest
from datetime import datetime

from fastapi import HTTPException

from app.utils.date_utils import parse_date, parse_datetime, format_iso
from app.utils.errors import (
    bad_request_error,
    unauthorized_error,
    not_found_error,
    internal_server_error,
)


# =========================================================================
# date_utils
# =========================================================================

class TestParseDate:
    """Test parse_date helper."""

    def test_valid_date_default_format(self):
        result = parse_date("2024-06-15")
        assert result is not None
        assert result.year == 2024
        assert result.month == 6
        assert result.day == 15

    def test_valid_date_custom_format(self):
        result = parse_date("15/06/2024", fmt="%d/%m/%Y")
        assert result is not None
        assert result.day == 15

    def test_invalid_date_returns_none(self):
        assert parse_date("not-a-date") is None

    def test_empty_string_returns_none(self):
        assert parse_date("") is None

    def test_none_like_empty_returns_none(self):
        # Empty string is falsy in Python
        assert parse_date("") is None

    def test_wrong_format_returns_none(self):
        # Provide a date in DD-MM-YYYY but default expects YYYY-MM-DD
        assert parse_date("15-06-2024") is None


class TestParseDatetime:
    """Test parse_datetime helper."""

    def test_valid_datetime_default_format(self):
        result = parse_datetime("2024-06-15 10:30:00")
        assert result is not None
        assert result.hour == 10
        assert result.minute == 30

    def test_valid_datetime_custom_format(self):
        result = parse_datetime("15/06/2024 10:30", fmt="%d/%m/%Y %H:%M")
        assert result is not None
        assert result.year == 2024

    def test_invalid_datetime_returns_none(self):
        assert parse_datetime("definitely not a datetime") is None

    def test_empty_string_returns_none(self):
        assert parse_datetime("") is None


class TestFormatIso:
    """Test format_iso helper."""

    def test_valid_datetime_formatted(self):
        dt = datetime(2024, 6, 15, 10, 30, 0)
        result = format_iso(dt)
        assert result == "2024-06-15T10:30:00"

    def test_none_returns_none(self):
        assert format_iso(None) is None

    def test_round_trip(self):
        """parse_datetime ➜ format_iso should produce a valid ISO string."""
        dt = parse_datetime("2024-01-01 00:00:00")
        iso = format_iso(dt)
        assert iso is not None
        assert "2024-01-01" in iso


# =========================================================================
# Error helpers
# =========================================================================

class TestErrorHelpers:
    """Verify each error helper raises the correct HTTPException."""

    def test_bad_request_error(self):
        with pytest.raises(HTTPException) as exc_info:
            bad_request_error("Invalid input")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Invalid input"

    def test_unauthorized_error_default(self):
        with pytest.raises(HTTPException) as exc_info:
            unauthorized_error()
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Unauthorized"

    def test_unauthorized_error_custom_message(self):
        with pytest.raises(HTTPException) as exc_info:
            unauthorized_error("Token expired")
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Token expired"

    def test_not_found_error_default(self):
        with pytest.raises(HTTPException) as exc_info:
            not_found_error()
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Resource not found"

    def test_not_found_error_custom_message(self):
        with pytest.raises(HTTPException) as exc_info:
            not_found_error("User not found")
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"

    def test_internal_server_error_default(self):
        with pytest.raises(HTTPException) as exc_info:
            internal_server_error()
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "An unexpected error occurred"

    def test_internal_server_error_custom_message(self):
        with pytest.raises(HTTPException) as exc_info:
            internal_server_error("DB connection lost")
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "DB connection lost"
