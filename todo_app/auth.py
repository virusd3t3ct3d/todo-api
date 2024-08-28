from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional
import os

# Secret key generation
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Handle potential exceptions from passlib, like if the hash is in an unexpected format
        print(f"Error verifying password: {e}")
        return False

def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        # Handle potential exceptions from passlib
        print(f"Error hashing password: {e}")
        raise e

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except (TypeError, ValueError) as e:
        # Handle JWT encoding errors properly
        print(f"Error encoding JWT: {e}")
        raise e  # Re-raise the exception to handle it appropriately in the calling code
