from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

# database table
class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    # one user can have many book
    books: list["Book"] = Relationship(back_populates="owner")


# request body for creating a user
class UserCreate(SQLModel):
    name: str
    email: str
    college: str


# response body
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str


# avoid circular import
from models.book import Book
User.model_rebuild()