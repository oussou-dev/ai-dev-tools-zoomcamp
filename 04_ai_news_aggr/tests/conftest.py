import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing.

    This fixture:
    1. Creates an in-memory SQLite database
    2. Creates all tables defined in models
    3. Yields a session for tests to use
    4. Tears down the database after the test
    """
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")

    # Create all tables
    Base.metadata.create_all(engine)

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create and yield session
    session = SessionLocal()
    yield session

    # Cleanup
    session.close()
    Base.metadata.drop_all(engine)
