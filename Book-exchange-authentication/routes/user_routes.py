from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from models.user import UserCreate, UserRead, User
from database import get_session
from auth import verify_api_key

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/",response_model=UserRead)
def create_user(
    user_data: UserCreate,
    api_key:str = Depends(verify_api_key),
    session: Session = Depends(get_session)
    ):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users