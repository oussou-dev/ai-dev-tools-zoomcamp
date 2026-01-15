import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()


def get_database_url() -> str:
    """
    Construct the PostgreSQL connection string from environment variables.
    
    Returns:
        str: The database connection URL in the format postgresql://user:password@host:port/db
    """
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "ai_news_aggregator")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


# Create the database engine
engine = create_engine(get_database_url())

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """
    Get a new database session.
    
    Returns:
        Session: A new SQLAlchemy session instance
    """
    return SessionLocal()
