# Business logic
from sqlalchemy.orm import Session
from models import User
from schemas import UserRegister
from utils import hash_password, verify_password


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
        password = hashed_password
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