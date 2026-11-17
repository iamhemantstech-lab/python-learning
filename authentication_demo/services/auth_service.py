# Business logic
from datetime import datetime
from sqlalchemy.orm import Session
from models import User, RefreshToken
from schemas import UserRegister
from utils import hash_password, verify_password, decode_access_token


def register_user(user_data: UserRegister, db: Session):

    # check whether email already exists
    user_exist = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if user_exist:
        print("User already exists!!")
        return None

    # hash password
    hashed_password = hash_password(user_data.password)

    # create user object
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = hashed_password,
        mobile_number = user_data.mobile_number,
        city = user_data.city,
        state = user_data.state,
        country = user_data.country
    )

    # save user
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except Exception:
        db.rollback()
        raise


def authenticate_user(email: str, password: str, db: Session):

    # find user by email
    find_user = db.query(User).filter(
        User.email == email
    ).first()

    # check user exists
    if not find_user:
        return None

    # verify password
    if not verify_password(password, find_user.password):
        return None

    # check account status whether active or not
    if not find_user.is_active:
        return None

    return find_user


def save_refresh_token(user_id: int, token: str, expires_at: datetime, db: Session) -> RefreshToken:
    """Stores a newly generated refresh token in MySQL."""
    refresh_record = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        is_revoked=False
    )
    db.add(refresh_record)
    db.commit()
    db.refresh(refresh_record)
    return refresh_record


def verify_and_use_refresh_token(token: str, db: Session) -> User | None:
    """
    Validates a refresh token:
    1. Checks JWT signature & expiration.
    2. Ensures token type is 'refresh'.
    3. Confirms token exists in MySQL and is not revoked.
    """
    payload = decode_access_token(token)
    if payload is None:
        return None

    # Ensure this token was issued specifically as a refresh token
    if payload.get("type") != "refresh":
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    # Check database record
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False
    ).first()

    if not db_token:
        return None

    # Find the corresponding user
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        return None

    return user


def revoke_refresh_token(token: str, db: Session) -> bool:
    """Revokes a refresh token in MySQL (used on logout)."""
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if db_token:
        db_token.is_revoked = True
        db.commit()
        return True

    return False
