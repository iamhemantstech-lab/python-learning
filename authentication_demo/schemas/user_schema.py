# Request and response validation
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# 1. Request Schema: Validates incoming data during registration
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of user")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=150, description="Plain text password")


# Alias for backward compatibility
UserSchema = UserRegister


# 2. Response Schema for User: Never includes the password or password hash
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    # Pydantic v2: allows reading directly from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)


# 3. Response Schema for Registration Endpoint
class RegisterResponse(BaseModel):
    message: str = "User registered successfully"
    user: UserResponse

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 4. Response Schema for Login Endpoint (JWT Token)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
