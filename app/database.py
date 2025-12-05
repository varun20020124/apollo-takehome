"""
1. Creates the SQLite engine (vehicles.db) with SQLAlchemy.
2. Creates a SessionLocal factory used to open/close DB sessions.
3. Provides the get_db() dependency used in FastAPI routes.
4. Defines Base = declarative_base() for SQLAlchemy models to inherit.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file used by the application
DATABASE_URL = "sqlite:///./vehicles.db"

# SQLAlchemy engine that manages the DB connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Factory that creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all SQLAlchemy ORM models
Base = declarative_base()


# Dependency that provides a database session to FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db # Makes the session available inside the request
    finally:
        db.close() 
