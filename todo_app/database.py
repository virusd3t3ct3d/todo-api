from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import urllib.parse

# Fetch environment variables with default fallbacks or raise error if not found
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise EnvironmentError("Database configuration environment variables are not set properly.")

# Use environment variables for database credentials
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USERNAME}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # Log the error properly or handle it as needed
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception to ensure proper error handling
    finally:
        db.close()
