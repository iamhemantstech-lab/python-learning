from sqlalchemy.orm import Session
from models import User
from schemas import UserUpdate


def get_user_by_id(user_id: int, db: Session) -> User | None:
    """Fetches a user by their primary key ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(email: str, db: Session) -> User | None:
    """Fetches a user by their email address."""
    return db.query(User).filter(User.email == email).first()


def update_user_profile(user_id: int, update_data: UserUpdate, db: Session) -> User | None:
    """
    Updates user profile fields with partial data (PATCH semantics).
    Only fields explicitly provided in the request body are modified.
    """
    user = get_user_by_id(user_id, db)
    if not user:
        return None

    # exclude_unset=True ensures only fields sent by the client are updated
    fields_to_update = update_data.model_dump(exclude_unset=True)
    for field_name, value in fields_to_update.items():
        setattr(user, field_name, value)

    db.commit()
    db.refresh(user)
    return user
