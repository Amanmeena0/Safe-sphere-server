"""
Shared test fixtures for the SafeSphere test suite.

Provides:
- In-memory SQLite database for fast, isolated testing
- FastAPI TestClient with overridden DB dependency
- Factory helpers for creating test users and FIR records
"""
import os
import pytest
from unittest.mock import MagicMock

# Set environment variables BEFORE any app imports to prevent
# Settings from trying to connect to a real database or read .env
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("CLERK_SECRET_KEY", "")
os.environ.setdefault("CLERK_JWKS_URL", "")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.models.database import Base
from app.api.dependencies import get_db, get_current_user
from app.main import app
from app.models.models import User

import uuid
from datetime import datetime


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def engine():
    """Create a shared in-memory SQLite engine for the entire test session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db_session(engine) -> Session:
    """
    Provide a transactional database session that rolls back after each test.
    This keeps every test fully isolated.
    """
    connection = engine.connect()
    transaction = connection.begin()
    TestingSession = sessionmaker(bind=connection)
    session = TestingSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ---------------------------------------------------------------------------
# Auth / user fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def test_user(db_session: Session) -> User:
    """Insert and return a test user in the DB."""
    user = User(
        id=uuid.uuid4(),
        clerk_user_id="test_clerk_user_123",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        name="Test User",
        status="active",
        registration_date=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ---------------------------------------------------------------------------
# FastAPI TestClient fixture
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(db_session: Session, test_user: User) -> TestClient:
    """
    Return a TestClient with the DB and auth dependencies overridden.
    Every request will use the transactional db_session and skip
    real Clerk authentication.
    """

    def _override_get_db():
        yield db_session

    def _override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_current_user] = _override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture()
def unauthenticated_client(db_session: Session) -> TestClient:
    """
    Return a TestClient with DB override but WITHOUT auth override.
    Useful for testing that endpoints correctly reject unauthenticated requests.
    """

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture()
def mock_redis():
    """Return a MagicMock that impersonates a Redis client."""
    redis_mock = MagicMock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.delete.return_value = True
    return redis_mock
