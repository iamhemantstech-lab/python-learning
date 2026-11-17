# API endpoints
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    UserRegister,
    RegisterResponse,
    UserLogin,
    Token,
    RefreshTokenRequest
)
from services import (
    register_user,
    authenticate_user,
    save_refresh_token,
    verify_and_use_refresh_token,
    revoke_refresh_token
)
from utils import create_access_token, create_refresh_token
from config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication (Public)"]
)

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    new_user = register_user(user_data, db)

    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    return {
        "message": "User registered successfully",
        "user": new_user
    }

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(
        user_data.email,
        user_data.password,
        db
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 1. Generate short-lived Access Token (15 mins)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # 2. Generate long-lived Refresh Token (7 days)
    refresh_token, expires_at = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # 3. Store Refresh Token in MySQL database
    save_refresh_token(user.id, refresh_token, expires_at, db)

    # 4. Set HttpOnly Cookie (for Web Browsers / React / Next.js)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )

    # 5. Also return in JSON body (Option 1: easy testing in Swagger UI, Postman, Mobile)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_access_token(
    request_data: RefreshTokenRequest = None,
    refresh_token_cookie: str | None = Cookie(default=None, alias="refresh_token"),
    db: Session = Depends(get_db)
):
    print("request_data",request_data)
    print("refresh_token_cookie",refresh_token_cookie)
    """
    Exchanges an active refresh token for a brand new Access Token.
    Accepts token from JSON body OR HttpOnly Cookie automatically.
    """
    token_to_verify = None
    if request_data and request_data.refresh_token:
        token_to_verify = request_data.refresh_token
    elif refresh_token_cookie:
        token_to_verify = refresh_token_cookie

    if not token_to_verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing. Provide it in JSON body or as a cookie.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify against JWT signature, expiry, and database revocation status
    user = verify_and_use_refresh_token(token_to_verify, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired, or revoked refresh token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Issue fresh 15-minute Access Token
    new_access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return {
        "access_token": new_access_token,
        "refresh_token": token_to_verify,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    response: Response,
    request_data: RefreshTokenRequest = None,
    refresh_token_cookie: str | None = Cookie(default=None, alias="refresh_token"),
    db: Session = Depends(get_db)
):
    """
    Revokes the refresh token in MySQL and clears the HttpOnly cookie.
    """
    token_to_revoke = None
    if request_data and request_data.refresh_token and request_data.refresh_token != "string":
        token_to_revoke = request_data.refresh_token
    elif refresh_token_cookie:
        token_to_revoke = refresh_token_cookie

    if not token_to_revoke:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid refresh_token in the body or cookie to log out."
        )

    # Revoke in MySQL
    success = revoke_refresh_token(token_to_revoke, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found in database."
        )

    # Clear cookie from the browser
    response.delete_cookie(key="refresh_token")

    return {"message": "Logged out successfully. Refresh token revoked."}

