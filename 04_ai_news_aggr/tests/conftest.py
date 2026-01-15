import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base
from app.database.repository import Repository


@pytest.fixture(scope="function")
def test_db():
    """
    Create an in-memory SQLite database for testing.
    
    This fixture creates a fresh database for each test, creates all tables,
    yields a session for the test to use, and tears down the database after the test.
    """
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    # Yield session for test to use
    yield session
    
    # Cleanup: close session and dispose engine
    session.close()
    engine.dispose()


@pytest.fixture(scope="function")
def test_repository(test_db):
    """
    Create a Repository instance with a test database session.
    
    This fixture provides a ready-to-use Repository instance for testing
    database operations.
    """
    return Repository(session=test_db)
