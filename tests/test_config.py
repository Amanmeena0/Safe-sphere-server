"""
Tests for the Settings configuration class.

pydantic-settings reads from both .env files and OS environment variables.
We use monkeypatch to clear AWS-related env vars so we can test defaults properly.
"""
import pytest
from app.core.config import Settings


class TestSettings:
    """Test the Settings / config module."""

    def test_sqlalchemy_url_rewrites_postgres(self):
        """postgres:// prefix should be rewritten to postgresql+psycopg2://"""
        s = Settings(
            DATABASE_URL="postgres://user:pass@host/db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert s.sqlalchemy_database_url.startswith("postgresql+psycopg2://")

    def test_sqlalchemy_url_rewrites_postgresql(self):
        """postgresql:// prefix should also be rewritten."""
        s = Settings(
            DATABASE_URL="postgresql://user:pass@host/db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert s.sqlalchemy_database_url.startswith("postgresql+psycopg2://")

    def test_sqlalchemy_url_passthrough(self):
        """Other URL schemes (e.g. sqlite) should pass through unchanged."""
        s = Settings(
            DATABASE_URL="sqlite:///test.db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert s.sqlalchemy_database_url == "sqlite:///test.db"

    def test_sqlalchemy_url_preserves_credentials(self):
        """Credentials and path should be preserved after rewrite."""
        s = Settings(
            DATABASE_URL="postgres://admin:secret@db.example.com:5432/mydb",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert "admin:secret@db.example.com:5432/mydb" in s.sqlalchemy_database_url

    def test_default_cors_origins(self):
        """Settings should have default CORS origins."""
        s = Settings(
            DATABASE_URL="sqlite:///test.db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert len(s.BACKEND_CORS_ORIGINS) > 0
        assert "http://localhost:5173" in s.BACKEND_CORS_ORIGINS

    def test_default_redis_url(self, monkeypatch):
        monkeypatch.delenv("REDIS_URL", raising=False)
        s = Settings(
            DATABASE_URL="sqlite:///test.db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert s.REDIS_URL == "redis://localhost:6379/0"

    def test_optional_aws_fields_default_none(self, monkeypatch):
        """Without env vars, AWS fields should be None."""
        monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
        monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
        monkeypatch.delenv("AWS_S3_BUCKET", raising=False)
        monkeypatch.delenv("AWS_REGION", raising=False)
        s = Settings(
            DATABASE_URL="sqlite:///test.db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert s.AWS_ACCESS_KEY_ID is None
        assert s.AWS_SECRET_ACCESS_KEY is None
        assert s.AWS_S3_BUCKET is None

    def test_default_aws_region(self, monkeypatch):
        monkeypatch.delenv("AWS_REGION", raising=False)
        s = Settings(
            DATABASE_URL="sqlite:///test.db",
            SECRET_KEY="test",
            _env_file=None,
        )
        assert s.AWS_REGION == "us-east-1"

    def test_cors_contains_vercel_origin(self):
        s = Settings(
            DATABASE_URL="sqlite:///test.db",
            SECRET_KEY="test",
            _env_file=None,
        )
        vercel_origins = [o for o in s.BACKEND_CORS_ORIGINS if "vercel" in o]
        assert len(vercel_origins) > 0
