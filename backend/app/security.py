
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import jwt

from .config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # Create a copy so the original payload is not modified
    to_encode = data.copy()

    # Calculate token expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Add expiration to the token payload
    to_encode.update({"exp": expire})

    # Generate and sign the JWT
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str):
    # Decode the token and verify its signature and expiration
    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM]
    )

    return payload




password_hash = PasswordHash.recommended()
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)