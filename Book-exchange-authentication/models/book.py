from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int
    is_sold: bool = Field(default=False)

    # Foreign key to user table
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# request body for creating a book
class BookCreate(SQLModel):
    title: str
    author: str
    price: int
    user_id: int


# response body
class BookRead(SQLModel):
    id: int
    title: str
    author: str
    price: int
    user_id: int
    is_sold: bool

class BookUpdate(SQLModel):
    price: Optional[int] = None
    is_sold: Optional[bool] = None
    

# avoid circular import
from models.user import User
Book.model_rebuild()