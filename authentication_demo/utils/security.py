# Password hashing and JWT utilities
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# generate hash password
def hash_password(password:str) -> str:
    return password_hash.hash(password)

# verify password
def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# create jwt access token
from datetime import datetime, timedelta, timezone
import jwt
from config import settings

def create_access_token(data:dict) -> str:
    to_encode = data.copy()

    expiry_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp":expiry_time})

    token = jwt.encode(
        to_encode, # payload
        settings.SECRET_KEY, # secret key
        algorithm=settings.ALGORITHM # header - PyJWT uses THIS parameter to build the header {"alg": "HS256", "typ": "JWT"} is the exact standard
    )

    return token


# create jwt refresh token (Long-lived, e.g. 7 days)
def create_refresh_token(data: dict) -> tuple[str, datetime]:
    to_encode = data.copy()

    expiry_time = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({"exp": expiry_time, "type": "refresh"})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token, expiry_time


# decode and verify jwt access token
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None