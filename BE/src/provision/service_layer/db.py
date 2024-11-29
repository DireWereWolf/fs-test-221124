from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.provision import config

# Centralized session factory and engine creation
def get_postgres_engine():
    """Create and return the database engine."""
    return create_engine(config.get_postgres_uri(), echo=True)

# Bind the engine to a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_postgres_engine())

# Dependency function for FastAPI to get a database session
def get_session_local():
    """
    Dependency function for FastAPI to provide a database session.
    This works with FastAPI's Depends.
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db
    finally:
        db.close()
