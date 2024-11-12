from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base



# Define the database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./titanic.db"

# Create a new SQLAlchemy engine instance with the specified database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Set up a session factory with autocommit and autoflush disabled, bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for all models to inherit from
Base = declarative_base()

def get_db():
    # Dependency function to create a new database session
    db = SessionLocal()
    try:
        yield db  # Provide the session to the calling code
    finally:
        db.close()  # Ensure the session is closed after use
