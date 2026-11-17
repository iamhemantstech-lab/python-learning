from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserResponse, UserUpdate
from dependencies import get_current_user
from models import User
from services.user_service import update_user_profile

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    dependencies=[Depends(get_current_user)] # ALL routes in this file require a valid token!
)

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Protected route: Returns the profile of the currently logged-in user."""
    return current_user

@router.patch("/update", response_model=UserResponse)
def update_current_user_detail(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Protected route: Updates details for the currently logged-in user."""
    updated_user = update_user_profile(current_user.id, update_data, db)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user
